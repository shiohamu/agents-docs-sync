"""
Configuration Accessor Module
"""

from typing import Any


class ConfigAccessor:
    """
    Type-safe configuration accessor.
    Wraps the raw configuration dictionary and provides typed properties.
    """

    def __init__(self, config: dict[str, Any]):
        self._config = config

    @property
    def raw_config(self) -> dict[str, Any]:
        """Get raw configuration dictionary"""
        return self._config

    # Generation Settings
    @property
    def generation(self) -> dict[str, Any]:
        return self._config.get("generation", {})

    @property
    def generate_api_doc(self) -> bool:
        return self.generation.get("generate_api_doc", True)

    @property
    def update_readme(self) -> bool:
        return self.generation.get("update_readme", True)

    @property
    def generate_agents_doc(self) -> bool:
        return self.generation.get("generate_agents_doc", True)

    # LLM Settings
    @property
    def llm(self) -> dict[str, Any]:
        return self._config.get("llm", {})

    @property
    def llm_provider(self) -> str:
        return self.llm.get("provider", "openai")

    @property
    def llm_model(self) -> str:
        return self.llm.get("model", "gpt-4")

    @property
    def llm_temperature(self) -> float:
        return self.llm.get("temperature", 0.0)

    # Output Settings
    @property
    def output(self) -> dict[str, Any]:
        return self._config.get("output", {})

    @property
    def output_dir(self) -> str:
        return self.output.get("dir", "docs")

    @property
    def api_doc_dir(self) -> str:
        return self.output.get("api_doc_dir", "api")

    # RAG Settings
    @property
    def rag(self) -> dict[str, Any]:
        return self._config.get("rag", {})

    @property
    def rag_enabled(self) -> bool:
        return self.rag.get("enabled", False)
