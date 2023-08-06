"""
Attempt to determine a GitHub repository URL given a `pkg:gem` PURL string
"""
from __future__ import annotations

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class RubyGemsScorecardHelper(BaseScorecardHelper):
    """
    RubyGems Scorecard helper class
    """

    API_URL = "https://rubygems.org/api/v1"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using RubyGems API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl = PackageURL.from_string(purl_string)

        query_url = f"{self.API_URL}/gems/{purl.name}.json"

        self._logger.info(msg="Requesting component VCS URL from RubyGems API", indent_level=1)

        response = await self.query_api(query_url)
        return self.parse_response(
            search_data=response.json(),
            search_exp=(
                "[source_code_uri, homepage_uri, bug_tracker_uri, changelog_uri, wiki_uri] | "
                "[? not_null(@) && contains(@, 'github.com')]"
            ),
        )
