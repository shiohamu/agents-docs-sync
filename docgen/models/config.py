"""Configuration related Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .agents import AgentsConfigSection


class LanguagesConfig(BaseModel):
    """Languages configuration model."""

    auto_detect: bool = True
    preferred: list[str] = Field(default_factory=list)


class OutputConfig(BaseModel):
    """Output configuration model."""

    api_doc: str = "docs/api.md"
    readme: str = "README.md"
    agents_doc: str = "AGENTS.md"


class GenerationConfig(BaseModel):
    """Generation configuration model."""

    update_readme: bool = True
    generate_api_doc: bool = True
    generate_agents_doc: bool = True
    preserve_manual_sections: bool = True


class ExcludeConfig(BaseModel):
    """Exclude configuration model."""

    directories: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)


class CacheConfig(BaseModel):
    """Cache configuration model."""

    enabled: bool = True


class DebugConfig(BaseModel):
    """Debug configuration model."""

    enabled: bool = False


class DocgenConfig(BaseModel):
    """Main configuration model for docgen."""

    languages: LanguagesConfig = Field(default_factory=LanguagesConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    agents: "AgentsConfigSection" = Field(default_factory=lambda: AgentsConfigSection())
    exclude: ExcludeConfig = Field(default_factory=ExcludeConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    debug: DebugConfig = Field(default_factory=DebugConfig)
