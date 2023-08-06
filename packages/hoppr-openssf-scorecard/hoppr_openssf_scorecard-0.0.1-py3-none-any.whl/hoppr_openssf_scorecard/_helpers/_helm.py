"""
Attempt to determine a GitHub repository URL given a `pkg:helm` PURL string
"""
from __future__ import annotations

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class HelmScorecardHelper(BaseScorecardHelper):
    """
    Helm Scorecard helper class
    """

    API_URL = "https://artifacthub.io/api/v1/packages/helm"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using the Helm chart Artifact Hub REST API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl = PackageURL.from_string(purl_string)

        # If purl has no namespace, try substituting name for namespace
        query_url = "/".join([self.API_URL, purl.namespace or purl.name, purl.name])

        self._logger.info(msg="Requesting component VCS URL from Artifact Hub API", indent_level=1)

        response = await self.query_api(query_url)

        return self.parse_response(
            search_data=response.json(),
            search_exp="[home_url, links[*].url] | [] | [? contains(@, 'github.com')]",
        )
