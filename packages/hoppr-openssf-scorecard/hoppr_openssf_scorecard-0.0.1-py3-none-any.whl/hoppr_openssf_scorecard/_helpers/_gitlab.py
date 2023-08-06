"""
Search GitLab REST API for component repository URL
"""
from __future__ import annotations

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class GitLabScorecardHelper(BaseScorecardHelper):
    """
    GitLab Scorecard helper class
    """

    API_URL = "https://gitlab.com/api/v4"

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        ### NOT IMPLEMENTED

        Search for repository using GitLab REST API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        return []  # pragma: no cover
