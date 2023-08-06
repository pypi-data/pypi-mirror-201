"""
Pydantic models describing OpenSSF Scorecard JSON schema v2
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Documentation(BaseModel):
    """
    Documentation data model
    """

    short: str
    url: str


class ScorecardCheck(str, Enum):
    """
    Enum of Scorecard check names
    """

    BINARY_ARTIFACTS = "Binary-Artifacts"
    BRANCH_PROTECTION = "Branch-Protection"
    CI_TESTS = "CI-Tests"
    CII_BEST_PRACTICES = "CII-Best-Practices"
    CODE_REVIEW = "Code-Review"
    CONTRIBUTORS = "Contributors"
    DANGEROUS_WORKFLOW = "Dangerous-Workflow"
    DEPENDENCY_UPDATE_TOOL = "Dependency-Update-Tool"
    FUZZING = "Fuzzing"
    LICENSE = "License"
    MAINTAINED = "Maintained"
    PACKAGING = "Packaging"
    PINNED_DEPENDENCIES = "Pinned-Dependencies"
    SAST = "SAST"
    SECURITY_POLICY = "Security-Policy"
    SIGNED_RELEASES = "Signed-Releases"
    TOKEN_PERMISSIONS = "Token-Permissions"
    VULNERABILITIES = "Vulnerabilities"
    WEBHOOKS = "Webhooks"

    def __str__(self) -> str:
        return self.value


class Check(BaseModel):
    """
    Check data model
    """

    details: list[str] | None
    documentation: Documentation
    name: ScorecardCheck
    reason: str
    score: int | None = Field(None, ge=-1, le=10)


class Repo(BaseModel):
    """
    Repo data model
    """

    commit: str
    name: str


class Scorecard(BaseModel):
    """
    Scorecard data model
    """

    commit: str
    version: str


class ScorecardResponse(BaseModel):
    """
    ScorecardResponse data model describing response from OpenSSF Scorecard REST API
    """

    checks: list[Check]
    date: str
    metadata: list[str] | None = None
    repo: Repo
    score: float = Field(..., ge=0.0, le=10.0)
    scorecard: Scorecard
