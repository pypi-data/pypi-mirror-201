"""
Search GitHub REST API for component repository URL
"""
from __future__ import annotations

from datetime import datetime
from time import sleep

import jmespath
import trio

from packageurl import PackageURL

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper


class GitHubScorecardHelper(BaseScorecardHelper):
    """
    GitHub Scorecard helper class
    """

    API_URL = "https://api.github.com"

    @classmethod
    async def await_rate_limit_reset(cls) -> None:
        """
        Await rate limit reset for GitHub REST API if exceeded
        """
        response = await cls().query_api(
            query_url=f"{cls.API_URL}/rate_limit",
            headers={"accept": "application/vnd.github+json"},
        )

        search_rate_limit = jmespath.search(expression="resources.search", data=response.json())

        if search_rate_limit["remaining"] == 0:
            reset_time: int = search_rate_limit["reset"]
            await trio.sleep(reset_time - datetime.now().timestamp())

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using GitHub REST API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl = PackageURL.from_string(purl_string)

        query = f"{purl.name} in:name"

        # Attempt to intuit repository language to narrow search results
        language = self.purl_type_language.get(purl.type)

        if language is not None:
            " ".join([query, f"language:{language}"])

        # Speed bump to avoid exceeding rate limit
        sleep(1)
        await self.await_rate_limit_reset()

        self._logger.info(msg="Requesting component VCS URL from GitHub API", indent_level=1)

        response = await self.query_api(
            query_url=f"{self.API_URL}/search/repositories",
            params={"q": query},
            headers={"accept": "application/vnd.github+json"},
        )

        # Attempt to narrow results with name match
        results = jmespath.search(expression=f"items[? contains(name, '{purl.name}')]", data=response.json())

        if len(results) == 0:
            return []

        def _sort_results(sort_by: str) -> list[dict]:
            return list(jmespath.search(expression=f"[*] | sort_by(@, &{sort_by}) | reverse(@)", data=results))

        # Generate multiple lists of results sorted by different metrics
        by_forks, by_stars = map(_sort_results, ["forks", "watchers"])

        result_relevance: dict[str, float] = {}

        # Compute an average of each result's position in each list to determine relevance
        for idx, result in enumerate(by_forks):
            relevance: float = sum([idx, by_stars.index(result)]) / 2
            result_relevance[result["full_name"]] = relevance

        # Sort the GitHub API search results by relevance and take the lowest value
        sorted_results = list(dict(sorted(result_relevance.items(), key=lambda item: item[1])).keys())

        return [f"https://github.com/{sorted_results[0]}"]
