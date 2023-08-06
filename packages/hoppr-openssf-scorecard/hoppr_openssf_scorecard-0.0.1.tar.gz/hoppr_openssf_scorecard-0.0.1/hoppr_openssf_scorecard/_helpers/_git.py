"""
Attempt to determine a GitHub repository URL given a `pkg:git` PURL string
"""
from __future__ import annotations

from time import sleep
from typing import AsyncGenerator
from urllib.parse import quote_plus

import httpx

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper
from hoppr_openssf_scorecard._helpers._github import GitHubScorecardHelper
from hoppr_openssf_scorecard._helpers._gitlab import GitLabScorecardHelper


class GitScorecardHelper(BaseScorecardHelper):
    """
    Git Scorecard helper class
    """

    async def _repo_generator(self) -> AsyncGenerator[str, None]:
        """
        Asynchronous generator to yield Git repository URLs for a component
        """
        if self.context and len(self.context.repositories["git"] or []) > 0:
            for repo_obj in self.context.repositories["git"] or []:
                yield repo_obj.url
        else:
            for git_repo in ["https://github.com", "https://gitlab.com"]:
                yield git_repo

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Route component to GitHub/GitLab helper based on defined manifest repositories

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        results: list[str] = []
        purl = PackageURL.from_string(purl_string)

        purl_dict = purl.to_dict()
        purl_dict["name"] = purl_dict["name"].removesuffix(".git")
        purl = PackageURL(**purl_dict)

        # Attempt to search git APIs of manifest repositories
        async for git_repo in self._repo_generator():
            match git_repo:
                case github if "github.com" in github:
                    # Query string to search for repository with exact match
                    query = f"repo:{purl.namespace}/{purl.name}"
                    query_url = f"{GitHubScorecardHelper.API_URL}/search/repositories"

                    # Speed bump to avoid exceeding rate limit
                    sleep(1)
                    await GitHubScorecardHelper.await_rate_limit_reset()

                    self._logger.info(msg="Requesting component VCS URL from GitHub API")

                    try:
                        response = await self.query_api(
                            query_url=query_url,
                            params={"q": query},
                            headers={"accept": "application/vnd.github+json"},
                        )

                        results = self.parse_response(
                            search_data=response.json(),
                            search_exp="items[0] | not_null(html_url) && to_array(html_url)",
                        )

                        if results is not None:
                            break
                    except httpx.HTTPStatusError:
                        self._logger.warning(msg="Unable to find GitHub repository")
                        continue

                case gitlab if "gitlab.com" in gitlab:
                    project_id = quote_plus(f"{purl.namespace}/{purl.name}")

                    self._logger.info(msg="Requesting component VCS URL from GitLab API")

                    try:
                        response = await self.query_api(
                            query_url=f"{GitLabScorecardHelper.API_URL}/projects/{project_id}",
                        )

                        results = self.parse_response(
                            search_data=response.json(),
                            search_exp="not_null(web_url) && to_array(web_url)",
                            platform="gitlab.com",
                        )

                        if results is not None:
                            break
                    except httpx.HTTPStatusError:
                        self._logger.warning(msg="Unable to find GitLab repository")
                        continue
                case _:
                    results = []

        return results
