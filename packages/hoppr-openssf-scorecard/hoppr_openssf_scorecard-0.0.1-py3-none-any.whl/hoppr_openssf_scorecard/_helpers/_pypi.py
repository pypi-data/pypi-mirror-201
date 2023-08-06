"""
Attempt to determine a GitHub repository URL given a `pkg:pypi` PURL string
"""
from __future__ import annotations

from urllib.parse import urljoin

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class PyPIScorecardHelper(BaseScorecardHelper):
    """
    PyPI Scorecard helper class
    """

    API_URL = "https://pypi.org"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Attempt to get VCS repository URL by querying PyPI JSON API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl = PackageURL.from_string(purl_string)
        query_url = urljoin(base=self.API_URL, url="/".join(["pypi", purl.name, purl.version, "json"]))

        self._logger.info(msg="Requesting component VCS URL from PyPI JSON API", indent_level=1)

        response = await self.query_api(query_url)
        return self.parse_response(
            search_data=response.json(),
            search_exp=(
                "(not_null(info.home_page) && contains(info.home_page, 'github.com') && to_array(info.home_page)) || "
                "(info.project_urls | [Homepage, Source] | [? not_null(@) && contains(@, 'github.com')])"
            ),
        )
