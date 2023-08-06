"""
Hoppr plugin to populate SBOM with OpenSSF scorecard data
"""
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Literal, TypeAlias, final
from urllib.parse import urlparse

import httpx
import jmespath
import trio

from hoppr import (
    BomAccess,
    Component,
    ComponentCoverage,
    ExternalReference,
    HopprContext,
    HopprPlugin,
    Property,
    Result,
    hoppr_process,
    hoppr_rerunner,
)
from hoppr.mem_logger import MemoryLogger
from packageurl import PackageURL
from packageurl.contrib.purl2url import get_repo_url

from hoppr_openssf_scorecard import __version__
from hoppr_openssf_scorecard._helpers import (
    DebScorecardHelper,
    GitHubScorecardHelper,
    GitScorecardHelper,
    GolangScorecardHelper,
    HelmScorecardHelper,
    LibrariesIOScorecardHelper,
    MavenScorecardHelper,
    NPMScorecardHelper,
    PyPIScorecardHelper,
    RPMScorecardHelper,
    RubyGemsScorecardHelper,
)
from hoppr_openssf_scorecard.models.scorecard import ScorecardResponse
from hoppr_openssf_scorecard.models.types import HopprScorecardProperties

if TYPE_CHECKING:
    AnyHelper: TypeAlias = (
        DebScorecardHelper
        | GitHubScorecardHelper
        | GitScorecardHelper
        | GolangScorecardHelper
        | HelmScorecardHelper
        | LibrariesIOScorecardHelper
        | MavenScorecardHelper
        | NPMScorecardHelper
        | PyPIScorecardHelper
        | RPMScorecardHelper
        | RubyGemsScorecardHelper
        | None
    )

_SCORECARD_API_URL = "https://api.securityscorecards.dev"
_REQUEST_TIMEOUT = 30


class HopprScorecardPlugin(HopprPlugin):
    """
    Hoppr plugin to populate SBOM with OpenSSF scorecard data
    """

    bom_access: BomAccess = BomAccess.COMPONENT_ACCESS
    default_component_coverage = ComponentCoverage.NO_MORE_THAN_ONCE
    required_commands: list[str] = []
    supported_purl_types: list[str] = [
        "deb",
        "gem",
        "git",
        "github",
        "gitlab",
        "golang",
        "helm",
        "maven",
        "npm",
        "pypi",
        "rpm",
    ]

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.async_client = httpx.AsyncClient()
        self.scorecard_map: dict[Component, ScorecardResponse | None] = {}
        self.vcs_url_map: dict[str, list[str] | None] = {}

        self._logger = MemoryLogger(
            file_name=str(context.logfile_location),
            lock=context.logfile_lock,  # type: ignore[arg-type]
            log_level=context.log_level,
            flush_immed=True,
        )

    def _add_scorecard_properties(self, component: Component) -> Result:
        """
        Add scorecard metadata to component properties

        Args:
            component (Component): Component to modify
        """
        scorecard = self.scorecard_map.get(component)

        if scorecard is None:
            return Result.skip(message=f"No scorecard data available for component: '{component}'")

        if component.properties is None:
            component.properties = []

        properties = [
            Property(name=HopprScorecardProperties.DATE, value=scorecard.date),
            Property(name=HopprScorecardProperties.REPO_NAME, value=scorecard.repo.name),
            Property(name=HopprScorecardProperties.REPO_COMMIT, value=scorecard.repo.commit),
            Property(name=HopprScorecardProperties.SCORECARD_VERSION, value=scorecard.scorecard.version),
            Property(name=HopprScorecardProperties.SCORECARD_COMMIT, value=scorecard.scorecard.commit),
            Property(name=HopprScorecardProperties.SCORE, value=str(scorecard.score)),
        ]

        if scorecard.metadata is not None:
            properties.append(Property(name=HopprScorecardProperties.METADATA, value=", ".join(scorecard.metadata)))

        for check in scorecard.checks:
            if check.score is not None:
                properties.append(
                    Property(name=f"{HopprScorecardProperties.CHECK}:{check.name}", value=str(check.score))
                )

        component.properties.extend(properties)

        return Result.success(return_obj=component)

    def _add_vcs_url_external_reference(self, component: Component, repo_url: str) -> None:
        """
        Update an SBOM component with an ExternalReference to its discovered VCS URL

        Args:
            component (Component): Component object to modify
            repo_url (str): URL to add to the Component's externalReferences
        """
        if component.externalReferences is None:
            component.externalReferences = []  # pragma: no cover

        vcs_ref = ExternalReference(url=repo_url, type="vcs", comment=None, hashes=None)  # type: ignore[arg-type]
        component.externalReferences.append(vcs_ref)

    async def _component_generator(self) -> AsyncGenerator[Component, None]:
        """
        Asynchronous generator to yield components from delivered SBOM
        """
        for component in self.context.delivered_sbom.components:
            yield component

    async def _create_vcs_url_map(self) -> None:
        """
        Populate mapping of Component objects to respective VCS repository URL
        """
        async for component in self._component_generator():
            if component.purl is None:
                component_str = f"{component.name}{f'@{component.version}' if component.version else ''}"
                self._logger.warning(msg=f"Component {component_str} is missing the 'purl' property.")
                continue

            component_header = "@".join(filter(None, [component.name, component.version]))
            self._logger.info(msg=f"{'-' * 4} Component: {component_header} {'-' * 50}")
            self._logger.info(msg="Checking component metadata for VCS URL")
            self._logger.flush()

            self.vcs_url_map[component.purl] = self._get_repo_from_component(component)

            # If VCS repo URL was found in component metadata, continue to next component
            if self.vcs_url_map[component.purl]:
                self._logger.info(msg=f"Found repository URL: '{self.vcs_url_map[component.purl]}'", indent_level=2)
                continue

            # Search for VCS repository URL based on component type
            purl: PackageURL = PackageURL.from_string(component.purl)  # pyright: ignore[reportGeneralTypeIssues]

            helper: AnyHelper = None

            match purl.type:
                case "deb":
                    helper = DebScorecardHelper(self.context)
                case "gem":
                    helper = RubyGemsScorecardHelper(self.context)
                case "git":
                    helper = GitScorecardHelper(self.context)
                case "github" | "gitlab":
                    self.vcs_url_map[component.purl] = get_repo_url(component.purl)
                case "golang":
                    helper = GolangScorecardHelper(self.context)
                case "helm":
                    helper = HelmScorecardHelper(self.context)
                case "maven":
                    helper = MavenScorecardHelper(self.context)
                case "npm":
                    helper = NPMScorecardHelper(self.context)
                case "pypi":
                    helper = PyPIScorecardHelper(self.context)
                case "rpm":
                    helper = RPMScorecardHelper(self.context)
                case _:
                    self._logger.warning(msg=f"No helper exists for PURL type: '{purl.type}'")

            # Specialized search for VCS repo URL based on PURL type
            if helper is not None:
                self.vcs_url_map[component.purl] = await helper.get_vcs_repo_url(component.purl)

            # If not found, search for repo using the Libraries.io API
            if not self.vcs_url_map[component.purl]:
                helper = LibrariesIOScorecardHelper(self.context)
                self.vcs_url_map[component.purl] = await helper.get_vcs_repo_url(component.purl)

            # Last-ditch effort to search for repo using the GitHub API
            if not self.vcs_url_map[component.purl]:
                helper = GitHubScorecardHelper(self.context)
                self.vcs_url_map[component.purl] = await helper.get_vcs_repo_url(component.purl)

            if not self.vcs_url_map[component.purl]:
                self._logger.warning(msg=f"Unable to find repository URL for component '{component.purl}'")
                continue

            # Update component in SBOM with an externalReference of type "vcs" with repositories found
            for repo_url in self.vcs_url_map[component.purl] or []:
                self._logger.info(msg=f"Found repository URL: '{repo_url}'")
                self._add_vcs_url_external_reference(component, repo_url)

        await self.async_client.aclose()

    def _get_repo_from_component(self, component: Component) -> list[str] | None:
        """
        Check a Component for a `externalReferences` URL of type `vcs` or `distribution`

        Args:
            component (Component): Component object to process

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        # Search for VCS repository URL in component metadata
        found_repos: list[str] | None = jmespath.search(
            expression=(
                "externalReferences[*] | "
                "[? type=='distribution' || type=='vcs'].url | "
                "[? not_null(@) && contains(@, 'github.com')]"
            ),
            data=component.dict(by_alias=True),
        )

        return found_repos

    async def _query_scorecard_api(
        self,
        repo_owner: str,
        repo_name: str,
        platform: Literal["github.com", "gitlab.com"] = "github.com",
    ) -> ScorecardResponse | None:
        """
        Query the OpenSSF Scorecard REST API

        Args:
            repo_owner (str): Name of the owner/organization of the repository
            repo_name (str): Name of the repository
            platform(str): One of "github.com", "gitlab.com". Defaults to "github.com".

        Returns:
            ScorecardResponse | None: Response data; None if HTTPError was raised
        """
        repo_lookup = "/".join([platform, repo_owner, repo_name])
        query_url = f"{_SCORECARD_API_URL}/projects/{repo_lookup}"

        self._logger.info(msg=f"Requesting Scorecard data for repository '{repo_lookup}'")
        self._logger.debug(msg="Request data:", indent_level=1)
        self._logger.debug(msg=f"url: {query_url}", indent_level=2)

        response = await self.async_client.get(url=query_url, follow_redirects=True, timeout=_REQUEST_TIMEOUT)

        self._logger.debug(msg=f"response status code: {response.status_code}", indent_level=2)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            self._logger.warning(f"Scorecard data not found for repository '{repo_lookup}'")
            return None

        return ScorecardResponse(**response.json())

    @hoppr_process
    @hoppr_rerunner
    def pre_stage_process(self) -> Result:
        """
        Preprocess SBOM components to determine VCS repository URL
        """
        HopprScorecardPlugin.bom_access = BomAccess.FULL_ACCESS

        purl_strings: list[str] = jmespath.search(
            expression="components[*].purl",
            data=self.context.delivered_sbom.dict(),
        )

        self.vcs_url_map.update(dict.fromkeys(purl_strings))

        trio.run(self._create_vcs_url_map)
        return Result.success(return_obj=self.context.delivered_sbom)

    @final
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """
        Populate a component with OpenSSF Scorecard data
        """
        repo_urls = self._get_repo_from_component(comp)

        if not comp.purl or not repo_urls:
            return Result.skip(message="No VCS repository metadata associated with component.")

        for vcs_url in repo_urls or []:
            parsed_url = urlparse(vcs_url)
            repo_owner, repo_name = str(parsed_url.path).removesuffix(".git").rsplit("/", maxsplit=1)
            repo_owner = repo_owner.strip("/")
            repo_name = repo_name.strip("/")

            # Request scorecard data
            self.scorecard_map[comp] = trio.run(self._query_scorecard_api, repo_owner, repo_name, parsed_url.netloc)

            if self.scorecard_map[comp] is not None:
                return self._add_scorecard_properties(comp)

        return Result.skip(message=f"Scorecard data not found for component: '{comp.purl}'")

    def get_version(self) -> str:
        """
        Get plugin version

        Returns:
            str: The version of the plugin
        """
        return __version__
