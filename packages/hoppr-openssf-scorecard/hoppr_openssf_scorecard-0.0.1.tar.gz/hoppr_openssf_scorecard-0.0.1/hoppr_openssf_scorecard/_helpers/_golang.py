"""
Attempt to determine a GitHub repository URL given a `pkg:golang` PURL string
"""
from __future__ import annotations

import os

from urllib.parse import quote_plus, urljoin

import jmespath

from hoppr import Credentials
from packageurl import PackageURL
from pydantic import SecretStr

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper
from hoppr_openssf_scorecard._helpers._libraries import LibrariesIOScorecardHelper


class GolangScorecardHelper(BaseScorecardHelper):
    """
    Golang Scorecard helper class
    """

    API_URL = "https://proxy.golang.org"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository in Golang proxy

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

        if purl.namespace.startswith("github.com/"):
            return [f"https://{purl.namespace}/{purl.name}"]

        query_url = urljoin(base=self.API_URL, url="/".join([purl.namespace, purl.name, "@latest"]))

        self._logger.info(msg="Requesting component VCS URL from Golang proxy", indent_level=1)

        response = await self.query_api(query_url)
        response_dict = response.json()

        repo_url: str | None = jmespath.search(
            expression="Origin.URL | not_null(@) && contains(@, 'github.com') && @",
            data=response_dict,
        )

        if not repo_url:
            # Search by Go platform on Libraries.IO
            self._logger.info(msg="Searching for component by Go platform on Libraries.io API", indent_level=1)

            name = quote_plus("/".join(filter(None, [purl.namespace, purl.name])))
            query_params: dict[str, str | SecretStr] = {"api_key": api_key}

            response = await self.query_api(
                query_url=f"{LibrariesIOScorecardHelper.API_URL}/go/{name}",
                params=query_params,
            )

            repo_url = jmespath.search(expression="repository_url", data=response.json())
            if not repo_url:
                return []

        response_dict.update({"Origin": {"URL": repo_url}})

        return self.parse_response(
            search_data=response_dict,
            search_exp="Origin.URL | not_null(@) && contains(@, 'github.com') && to_array(@)",
        )
