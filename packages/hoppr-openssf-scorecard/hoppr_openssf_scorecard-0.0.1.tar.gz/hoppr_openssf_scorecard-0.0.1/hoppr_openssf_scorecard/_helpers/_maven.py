"""
Attempt to determine a GitHub repository URL given a `pkg:maven` PURL string
"""
from __future__ import annotations

import os

from typing import Any, OrderedDict

import jmespath
import xmltodict

from hoppr import Credentials
from packageurl import PackageURL
from pydantic import SecretStr

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper
from hoppr_openssf_scorecard._helpers._libraries import LibrariesIOScorecardHelper


class MavenScorecardHelper(BaseScorecardHelper):
    """
    Maven Scorecard helper class
    """

    API_URL = "https://search.maven.org/remotecontent"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:  # pylint: disable=too-many-locals
        """
        Search for repository using Maven remote content API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        # pylint: disable=duplicate-code

        if credentials := Credentials.find(url=LibrariesIOScorecardHelper.API_URL):
            api_key = credentials.password
        else:
            try:
                api_key = SecretStr(os.environ["LIBRARIES_API_KEY"])
            except KeyError as ex:
                raise EnvironmentError(
                    f"Either a credentials file with an entry for '{LibrariesIOScorecardHelper.API_URL}' "
                    "or the environment variable LIBRARIES_API_KEY must be set to use this plugin."
                ) from ex

        purl = PackageURL.from_string(purl_string)

        group_path = "/".join(purl.namespace.split("."))
        filepath = "/".join([group_path, purl.name, purl.version, f"{purl.name}-{purl.version}.pom"])

        self._logger.info(msg="Requesting component VCS URL from Maven remote content API", indent_level=1)

        response = await self.query_api(f"{self.API_URL}?filepath={filepath}")
        pom_dict: OrderedDict[str, Any] = xmltodict.parse(xml_input=response.text, encoding="utf-8")

        repo_url: str | None = jmespath.search(expression="project.scm.connection", data=pom_dict)

        if not repo_url:
            # Search by Maven platform on Libraries.IO
            self._logger.info(msg="Searching for component by Maven platform on Libraries.io API", indent_level=1)

            name = ":".join(filter(None, [purl.namespace, purl.name]))
            query_params: dict[str, str | SecretStr] = {"api_key": api_key}

            response = await self.query_api(
                query_url=f"{LibrariesIOScorecardHelper.API_URL}/maven/{name}",
                params=query_params,
            )

            repo_url = jmespath.search(expression="repository_url", data=response.json())

        match repo_url:
            case str(github_url) if "github.com" in github_url:
                # Strip schemes such as "scm:git:git://" and replace with "https://"
                repo_url = f"https://{github_url.split(sep='://')[-1]}"
            case str(gitbox_url) if "gitbox.apache.org" in gitbox_url:
                # Convert Apache gitbox URL to its mirrored GitHub repo. For example:
                # scm:git:http://gitbox.apache.org/repos/asf/<ARTIFACT>.git -> https://github.com/apache/<ARTIFACT>
                repo_url = f"https://github.com/apache/{gitbox_url.split('/')[-1]}".removesuffix(".git")
            case not_found if not_found is None:
                return []

        pom_dict.update({"project": {"scm": {"connection": repo_url}}})

        return self.parse_response(
            search_data=pom_dict,
            search_exp="project.scm.connection | not_null(@) && contains(@, 'github.com') && to_array(@)",
        )
