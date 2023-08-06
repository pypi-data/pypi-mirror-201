"""
Base helper for attempting to determine GitHub repository URLs
"""
from __future__ import annotations

import re

from typing import Literal
from urllib.parse import urlparse

import httpx
import jmespath

from hoppr import HopprContext
from hoppr.mem_logger import MemoryLogger
from pydantic import SecretStr

REQUEST_TIMEOUT = 30


class BaseScorecardHelper:
    """
    BaseScorecardHelper class
    """

    API_URL = ""

    async_client = httpx.AsyncClient()

    purl_type_language = {
        "cargo": "Rust",
        "cocoapods": "Swift,Objective-C",
        "composer": "PHP",
        "conan": "C,C++",
        "conda": "Python",
        "cran": "R",
        "gem": "Ruby,Java",
        "golang": "Go",
        "hackage": "Haskell",
        "hex": "Elixir,Erlang",
        "huggingface": "Python",
        "maven": "Java",
        "mlflow": "Jupyter Notebook,Python",
        "npm": "JavaScript",
        "nuget": "C#,C++,F#,Visual Basic",
        "pub": "Dart",
        "pypi": "Python",
        "qpkg": "C,C++,Java",
        "swift": "Swift",
    }

    def __init__(self, context: HopprContext | None = None) -> None:
        super().__init__()
        self.context = context
        self._logger = MemoryLogger(file_name="hoppr.log", lock=None)

        if context is not None:
            self._logger = MemoryLogger(  # pylint: disable=duplicate-code
                file_name=str(context.logfile_location),
                lock=context.logfile_lock,  # type: ignore[arg-type]
                log_level=context.log_level,
                flush_immed=True,
            )

    def _get_secret_values(self, data: dict[str, str | SecretStr]) -> dict[str, str] | None:
        """
        Get string values of SecretStr query params or headers

        Args:
            data (dict[str, str | SecretStr]): Data potentially containing SecretStr values

        Returns:
            dict[str, str] | None: SecretStr values replaced with plain text strings, or None if empty dict provided
        """
        if len(data.keys()) == 0:
            return None

        secret_data: dict[str, str] = {}

        for key, value in data.items():
            match value:
                case str():
                    secret_data[key] = value
                case SecretStr():
                    secret_data[key] = value.get_secret_value()

        return secret_data

    async def query_api(
        self,
        query_url: str,
        headers: dict[str, str | SecretStr] | None = None,
        params: dict[str, str | SecretStr] | None = None,
    ) -> httpx.Response:
        """
        Query the specified REST API and return the response

        Args:
            query_url (str): The URL to send the request
            headers (dict[str, str | SecretStr] | None, optional): Request headers. Defaults to None.
            params (dict[str, str | SecretStr] | None, optional): Request parameters. Defaults to None.

        Returns:
            httpx.Response: The response from the API endpoint
        """
        self._logger.debug(msg="Request data:", indent_level=1)
        self._logger.debug(msg=f"url: {query_url}", indent_level=2)
        self._logger.debug(msg=f"headers: {headers}", indent_level=2)
        self._logger.debug(msg=f"params: {params}", indent_level=2)

        expanded_headers = self._get_secret_values(headers or {})
        expanded_params = self._get_secret_values(params or {})

        response = await self.async_client.get(
            url=query_url,
            headers=expanded_headers,
            params=expanded_params,
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
        )

        self._logger.debug(msg=f"response status code: {response.status_code}", indent_level=2)

        response.raise_for_status()

        return response

    async def get_vcs_repo_url(self, purl_string: str) -> list[str]:  # pragma: no cover
        """
        Attempt to get VCS repository URL from PURL string

        Args:
            purl_string (str): Package URL of the component

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        raise NotImplementedError("Subclasses of BaseScorecardHelper must implement the `get_vcs_repo_url` method")

    def parse_response(
        self,
        search_data: dict | list[dict],
        search_exp: str,
        platform: Literal["github.com", "gitlab.com"] = "github.com",
    ) -> list[str]:
        """
        Parse the response from the API endpoint

        Args:
            search_data(dict | list[dict]): The data to parse
            search_exp(str): The JMESPath expression used to search the data
            platform(str): One of "github.com", "gitlab.com". Defaults to "github.com".

        Returns:
            list[str]: VCS repository URLs for Scorecard API query
        """
        repo_urls: list[str] = jmespath.search(expression=search_exp, data=search_data) or []

        for idx, url in enumerate(repo_urls):
            if "git@" in url:
                # Parse SSH git protocol URLs, e.g.
                #   "git@github.com:<owner>/<project>.git"
                #   "git+ssh://git@github.com/<owner>/<project>.git"
                url = url.split("git@")[-1]
                url = "/".join(url.split(":", maxsplit=1))
                url = f"https://{url}"

            if str(urlparse(url=url).hostname).endswith(platform):
                # Strip additional trailing URL path segments after "github.com/<repo owner>/<repo name>"
                match = re.match(pattern=f"(.*{re.escape(platform)}/[\\w-]+/[\\w-]+)/?.*", string=url)
                if match is not None:
                    url = match.group(1)

            repo_urls[idx] = url

        return repo_urls
