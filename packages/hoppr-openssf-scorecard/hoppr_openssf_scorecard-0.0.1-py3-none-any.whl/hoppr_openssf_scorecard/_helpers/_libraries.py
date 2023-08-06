"""
Search Libraries.io REST API for component repository URL
"""
from __future__ import annotations

import os

from time import sleep
from typing import Any

import jmespath

from hoppr import Credentials
from packageurl import PackageURL
from pydantic import SecretStr

from hoppr_openssf_scorecard._helpers._base import BaseScorecardHelper
from hoppr_openssf_scorecard.models.libraries import LibrariesIOResponse, LibrariesIOResponseItem

_RELEVANCE_THRESHOLD = 2.0


class LibrariesIOScorecardHelper(BaseScorecardHelper):
    """
    Libraries.io Scorecard helper class
    """

    API_URL = "https://libraries.io/api"

    async def _get_query_results(self, purl: PackageURL) -> list[dict[str, Any]]:
        """
        Collect all paginated query results

        Args:
            purl (PackageURL): Package URL object

        Raises:
            EnvironmentError: No credentials file supplied and LIBRARIES_API_KEY environment variable not set

        Returns:
            list[dict[str, Any]]: The collected results data
        """
        if credentials := Credentials.find(url=self.API_URL):
            api_key = credentials.password
        else:
            try:
                api_key = SecretStr(os.environ["LIBRARIES_API_KEY"])
            except KeyError as ex:
                raise EnvironmentError(
                    f"Either a credentials file with an entry for '{self.API_URL}' or the "
                    "environment variable LIBRARIES_API_KEY must be set to use this plugin."
                ) from ex

        query_url = f"{self.API_URL}/search"
        query_params = {"q": purl.name, "api_key": api_key, "per_page": "100", "page": "1"}

        # Attempt to intuit repository language to narrow search results
        language = self.purl_type_language.get(purl.type)
        if language is not None:
            query_params["languages"] = language

        response = await self.query_api(query_url=query_url, params=query_params)
        results_list: list[dict] = response.json()

        # Attempt to narrow results down to exact name match
        exact_matches: list[dict] = jmespath.search(expression=f"[*] | [? name == '{purl.name}']", data=results_list)

        while response.json():
            if len(exact_matches) > 1:
                self._logger.warning(
                    msg=(
                        f"More than one exact name match for component '{purl.name}'. "
                        "Correct VCS repository URL can't be reliably determined."
                    )
                )
                return []

            # Speed bump to avoid exceeding rate limit
            sleep(1)

            # Get the next page of results
            query_params["page"] = str(int(query_params["page"]) + 1)
            response = await self.query_api(query_url=query_url, params=query_params)

            exact_matches.extend(jmespath.search(expression=f"[? name == '{purl.name}']", data=response.json()))
            results_list.extend(response.json())

        return exact_matches if exact_matches else results_list

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:
        """
        Search for repository using Libraries.io REST API

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        purl: PackageURL = PackageURL.from_string(purl_string)  # pyright: ignore

        self._logger.info(msg="Requesting component VCS URL from Libraries.io API", indent_level=1)

        results_list = await self._get_query_results(purl)

        # Attempt to narrow results down to matches containing name
        results = LibrariesIOResponse.parse_obj(
            jmespath.search(expression=f"[? contains(name, '{purl.name}')]", data=results_list)
        )

        if len(results) == 0:
            return []

        def _sort_results(sort_by: str) -> LibrariesIOResponse:
            return LibrariesIOResponse.parse_obj(
                jmespath.search(
                    expression=f"sort_by(@, &{sort_by}) | reverse(@)",
                    data=[result.dict() for result in results],
                )
            )

        # Generate multiple lists of results sorted by different metrics
        by_forks, by_rank, by_stars = map(_sort_results, ["forks", "rank", "stars"])

        result_relevance: dict[LibrariesIOResponseItem, float] = {}

        # Compute an average of each result's position in each list to determine relevance
        for idx, result in enumerate(results):
            values = [idx, by_forks.index(result), by_rank.index(result), by_stars.index(result)]
            result_relevance[result] = sum(values) / len(values)

        # Sort the Libraries.io search results by relevance and take the lowest value
        sorted_results = list(dict(sorted(result_relevance.items(), key=lambda item: item[1])).keys())
        self._logger.debug(msg=f"Best relevance score: {result_relevance[sorted_results[0]]}")

        # If lowest relevance score is not below threshold, don't consider it a match
        if result_relevance[sorted_results[0]] > _RELEVANCE_THRESHOLD:
            self._logger.warning(msg="Best match did not meet relevance requirement")
            return []

        return self.parse_response(search_data=sorted_results[0].dict(), search_exp="to_array(repository_url)")
