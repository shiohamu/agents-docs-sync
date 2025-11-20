"""ジェネレーターファクトリーモジュール"""

from pathlib import Path
import sys
from typing import Any

from .base_generator import BaseGenerator
from .utils.logger import get_logger

logger = get_logger("generator_factory")

# Expose concrete generator classes for test patching
try:
    from .generators.agents_generator import AgentsGenerator
    from .generators.api_generator import APIGenerator
    from .generators.readme_generator import ReadmeGenerator
except Exception:

    class APIGenerator:
        pass

    class ReadmeGenerator:
        pass

    class AgentsGenerator:
        pass


class GeneratorFactory:
    """ジェネレーターのファクトリークラス"""

    # Keep names to allow patching of symbols like APIGenerator, ReadmeGenerator, AgentsGenerator
    _generators = {
        "api": "APIGenerator",
        "readme": "ReadmeGenerator",
        "agents": "AgentsGenerator",
    }

    @classmethod
    def create_generator(
        cls,
        generator_type: str,
        project_root: Path,
        detected_languages: list[str],
        config: dict[str, Any],
    ) -> BaseGenerator:
        """指定されたタイプのジェネレーターを作成"""
        class_name = cls._generators.get(generator_type)
        if class_name is None:
            raise ValueError(f"Unknown generator type: {generator_type}")

        # Retrieve the actual class from the module's namespace to honor patches
        module = sys.modules[__name__]
        generator_class = getattr(module, class_name, None)
        if generator_class is None:
            raise ValueError(f"Generator class {class_name} not found for type: {generator_type}")

        return generator_class(project_root, detected_languages, config)

    @classmethod
    def get_available_generators(cls) -> list[str]:
        """利用可能なジェネレーターのリストを取得"""
        return list(cls._generators.keys())
