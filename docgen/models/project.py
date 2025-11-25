"""Project related Pydantic models."""

from typing import Any

from pydantic import BaseModel, Field


class ProjectInfo(BaseModel):
    """Project information model."""

    description: str | None = None
    build_commands: list[str] = Field(default_factory=list)
    test_commands: list[str] = Field(default_factory=list)
    dependencies: dict[str, list[str]] = Field(default_factory=dict)
    coding_standards: dict[str, Any] | None = None
    ci_cd_info: dict[str, Any] | None = None
    project_structure: dict[str, Any] | None = None
