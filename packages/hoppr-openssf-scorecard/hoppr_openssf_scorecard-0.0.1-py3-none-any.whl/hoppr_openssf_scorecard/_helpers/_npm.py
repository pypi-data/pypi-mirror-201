"""
Attempt to determine a GitHub repository URL given a `pkg:npm` PURL string
"""
from __future__ import annotations

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class NPMScorecardHelper(BaseScorecardHelper):
    """
    NPM Scorecard helper class
    """

    API_URL = "https://registry.npmjs.com"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using NPM Public Registry API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl = PackageURL.from_string(purl_string)

        # Construct request URL by joining base URL with component namespace (if not None) and name
        query_url = "/".join(filter(None, [self.API_URL, purl.namespace, purl.name]))

        self._logger.info(msg="Requesting component VCS URL from NPM Public Registry API", indent_level=1)

        response = await self.query_api(query_url)

        return self.parse_response(
            search_data=response.json(),
            search_exp="not_null(repository.url) && contains(repository.url, 'github.com') && to_array(repository.url)",
        )
