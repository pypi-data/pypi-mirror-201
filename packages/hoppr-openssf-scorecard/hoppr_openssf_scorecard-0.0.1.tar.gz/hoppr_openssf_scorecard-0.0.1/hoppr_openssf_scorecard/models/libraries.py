"""
Pydantic models describing Libraries.io JSON response schema
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, NoneStr


class LibrariesIOResponseVersion(BaseModel, allow_population_by_field_name=True):
    """
    LibrariesIOResponseVersion data model
    """

    number: str
    published_at: str
    spdx_expression: NoneStr
    original_license: str | list[str] | None
    researched_at: Any
    repository_sources: list[str]


class LibrariesIOResponseItem(BaseModel, allow_population_by_field_name=True):
    """
    LibrariesIOResponseItem data model
    """

    dependent_repos_count: int
    dependents_count: int
    deprecation_reason: Any
    description: NoneStr
    forks: int
    homepage: NoneStr
    keywords: list[str]
    language: NoneStr
    latest_download_url: Any
    latest_release_number: NoneStr
    latest_release_published_at: str
    latest_stable_release_number: NoneStr
    latest_stable_release_published_at: NoneStr
    license_normalized: bool
    licenses: NoneStr
    name: str
    normalized_licenses: list[str]
    package_manager_url: NoneStr
    platform: str
    rank: int
    repository_license: NoneStr
    repository_status: Any
    repository_url: NoneStr
    stars: int
    status: Any
    versions: list[LibrariesIOResponseVersion]

    def __hash__(self) -> int:
        return hash(repr(self))


class LibrariesIOResponse(BaseModel, allow_population_by_field_name=True):
    """
    LibrariesIOResponseItem data model
    """

    __root__: list[LibrariesIOResponseItem] = Field(...)

    def __getattr__(self, name: str) -> Any:
        return self.__root__.__getattribute__(name)

    def __getitem__(self, item: int) -> LibrariesIOResponseItem:
        return self.__root__[item]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self) -> int:
        return len(self.__root__)

    def __repr__(self) -> str:
        return f"LibrariesIOResponse({self.__root__})"  # pragma: no cover


LibrariesIOResponseItem.update_forward_refs()
