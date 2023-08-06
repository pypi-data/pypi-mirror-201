"""
Attempt to determine a GitHub repository URL given a `pkg:deb` PURL string
"""
from __future__ import annotations

import jmespath

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class DebScorecardHelper(BaseScorecardHelper):
    """
    Deb Scorecard helper class
    """

    DEBIAN_API_URL = "https://sources.debian.org/api"
    LAUNCHPAD_API_URL = "https://api.launchpad.net/1.0"

    async def _query_debian_api(self, purl: PackageURL) -> list[str]:
        """
        Search for repository using Debian sources API

        Args:
            purl (PackageURL): Package URL object

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        # Verify matching package name in Debian sources
        query_url = f"{self.DEBIAN_API_URL}/search/{purl.name}"

        self._logger.info(msg="Requesting component VCS URL from Debian Sources API", indent_level=1)

        response = await self.query_api(query_url)
        name = jmespath.search(
            expression=f"not_null(results.exact).name || (results.other[? name == '{purl.name.lower()}'].name | [0])",
            data=response.json(),
        )

        # Get latest package version
        query_url = f"{self.DEBIAN_API_URL}/src/{name or purl.name}"
        response = await self.query_api(query_url)
        version = jmespath.search(expression="versions[0].version", data=response.json())

        # Attempt to get package info, default to PURL package name and version if not found previously
        query_url = f"{self.DEBIAN_API_URL}/info/package/{name or purl.name}/{version or purl.version}"
        response = await self.query_api(query_url)

        return self.parse_response(
            search_data=response.json(),
            search_exp=(
                "pkg_infos | (not_null(vcs_browser) && contains(vcs_browser, 'github.com') && to_array(vcs_browser))"
            ),
        )

    async def _query_launchpad_api(self, purl: PackageURL) -> list[str]:
        """
        Search for repository using Ubuntu Launchpad API

        Args:
            purl (PackageURL): Package URL object

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        # Get source package information
        query_url = f"{self.LAUNCHPAD_API_URL}/ubuntu/+source/{purl.name}"

        self._logger.info(msg="Requesting component VCS URL from Ubuntu Launchpad API", indent_level=1)
        response = await self.query_api(query_url)

        upstream_product_link = jmespath.search(expression="upstream_product_link", data=response.json())
        if upstream_product_link is None:
            return []

        response = await self.query_api(upstream_product_link)

        return self.parse_response(
            search_data=response.json(),
            search_exp="not_null(homepage_url) && contains(homepage_url, 'github.com') && to_array(homepage_url)",
        )

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using Debian sources API or Launchpad API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl: PackageURL = PackageURL.from_string(purl_string)  # pyright: ignore

        match purl.namespace:
            case "debian":
                repo_url = await self._query_debian_api(purl)
            case "ubuntu":
                repo_url = await self._query_launchpad_api(purl)
            case _:
                raise ValueError("Namespace for 'pkg:deb' PURL must be one of 'debian', 'ubuntu'")

        return repo_url
