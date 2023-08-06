"""
Attempt to determine a GitHub repository URL given a `pkg:rpm` PURL string
"""
from __future__ import annotations

import gzip
import re

from typing import Any, AsyncGenerator, MutableMapping, OrderedDict

import httpx
import jmespath
import xmltodict

from hoppr import Credentials
from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class RPMScorecardHelper(BaseScorecardHelper):
    """
    RPM Scorecard helper class
    """

    CENTOS_REPODATA_URL = "http://mirror.centos.org/centos"
    FEDORA_REPODATA_URL = "https://dl.fedoraproject.org/pub/fedora/linux/releases"
    ROCKY_REPODATA_URL = "https://dl.rockylinux.org/pub/rocky"

    rpm_data: MutableMapping[str, OrderedDict[str, Any]] = {}

    async def _populate_rpm_data(self, repo: str, auth: httpx.BasicAuth | None = None) -> None:
        """
        Populate `rpm_data` dict for a repository

        Args:
            repo (str): The RPM repository URL
            auth (httpx.BasicAuth | None, optional): Authentication for repository URL, if required. Defaults to None.
        """
        query_url = f"{repo}/repodata/repomd.xml"

        response = await self.query_api(query_url)

        repomd_dict: OrderedDict[str, Any] = xmltodict.parse(xml_input=response.text, force_list=["data"])

        primary_xml_file = jmespath.search(
            expression="""repomd.data[? "@type"=='primary'].location."@href" | [0]""",
            data=repomd_dict,
        )

        if primary_xml_file is None:
            return

        self._logger.debug(msg=f"Found path to primary.xml file: '{primary_xml_file}'", indent_level=1)

        # Omit `auth` from AsyncClient.stream() args since None not allowed
        stream_args: dict[str, Any] = {
            "method": "GET",
            "url": f"{repo}/{primary_xml_file}",
            "headers": {"Accept-Encoding": "gzip"},
        }

        # Add `auth` to AsyncClient.stream() args if not None
        if auth is not None:
            stream_args["auth"] = auth

        self._logger.info(msg="Downloading metadata for all components in repository", indent_level=1)
        self._logger.debug(msg=f"Primary XML metadata file URL: {stream_args['url']}", indent_level=2)

        async with self.async_client.stream(**stream_args) as response:
            await response.aread()
            async for chunk in response.aiter_bytes():
                self.rpm_data[repo] = xmltodict.parse(xml_input=gzip.decompress(chunk), force_list=["package"])

    async def _repo_generator(self, arch: str, version: str) -> AsyncGenerator[str, None]:
        """
        Asynchronous generator to yield RPM repository URLs for a component

        Args:
            arch (str): Architecture of component
            version (str): Target platform version of component
        """
        if self.context and len(self.context.repositories["rpm"] or []) > 0:
            for repo_obj in self.context.repositories["rpm"]:
                yield repo_obj.url
        else:
            match version:
                case distro if ".el7" in distro:
                    for repo in ["os", "extras"]:
                        yield f"{self.CENTOS_REPODATA_URL}/7/{repo}/{arch}"
                case distro if ".el8" in distro:
                    for repo in ["AppStream", "BaseOS", "PowerTools", "extras"]:
                        yield f"{self.ROCKY_REPODATA_URL}/8/{repo}/{arch}/os"
                case distro if ".el9" in distro:
                    for repo in ["AppStream", "BaseOS", "CRB", "extras"]:
                        yield f"{self.ROCKY_REPODATA_URL}/9/{repo}/{arch}/os"
                case distro if ".fc" in distro:
                    match = re.search(pattern="^.*\\.fc(\\d+).*$", string=distro)
                    if match is None:
                        raise ValueError(f"PURL version '{distro}' must contain Fedora release version.")

                    yield f"{self.FEDORA_REPODATA_URL}/{match.group(1)}/Everything/{arch}/os"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Attempt to get VCS repository URL for RPM package

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        repo_urls: set[str] = set()

        purl = PackageURL.from_string(purl_string)

        arch = purl.qualifiers.get("arch", "x86_64")
        arch = "x86_64" if arch == "noarch" else arch

        async for repo in self._repo_generator(arch, purl.version):
            self._logger.info(msg=f"Searching RPM repository: '{repo}'")

            auth: httpx.BasicAuth | None = None
            credentials = Credentials.find(url=repo)

            if credentials is not None:
                auth = httpx.BasicAuth(
                    username=credentials.username,
                    password=credentials.password.get_secret_value(),
                )

            if self.rpm_data.get(repo) is None:
                self._logger.info(msg="Populating RPM repository metadata", indent_level=1)
                await self._populate_rpm_data(repo, auth)

            repo_url = self.parse_response(
                search_data=self.rpm_data[repo],
                search_exp=f"metadata.package[? name=='{purl.name}' && contains(url, 'github.com')].url",
            )

            if repo_url is not None:
                repo_urls.update(repo_url)

        return list(repo_urls)
