"""
Type definitions for Hoppr OpenSSF Scorecard plugin
"""
from __future__ import annotations

from enum import Enum


class HopprScorecardProperties(str, Enum):
    """
    Enum of scorecard data property names for use in SBOM
    """

    NAMESPACE = "hoppr:scorecard"
    CHECK = f"{NAMESPACE}:check"
    DATE = f"{NAMESPACE}:date"
    METADATA = f"{NAMESPACE}:metadata"
    REPO = f"{NAMESPACE}:repo"
    REPO_COMMIT = f"{REPO}:commit"
    REPO_NAME = f"{REPO}:name"
    SCORE = f"{NAMESPACE}:score"
    SCORECARD = f"{NAMESPACE}:scorecard"
    SCORECARD_COMMIT = f"{SCORECARD}:commit"
    SCORECARD_VERSION = f"{SCORECARD}:version"

    def __str__(self) -> str:
        return self.value
