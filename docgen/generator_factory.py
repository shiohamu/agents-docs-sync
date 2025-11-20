"""
ジェネレーターファクトリーモジュール
"""

from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator
from .generators.agents_generator import AgentsGenerator
from .generators.api_generator import APIGenerator
from .generators.readme_generator import ReadmeGenerator
from .utils.logger import get_logger

logger = get_logger("generator_factory")


class GeneratorFactory:
    """ジェネレーターのファクトリークラス"""

    _generators = {
        "api": APIGenerator,
        "readme": ReadmeGenerator,
        "agents": AgentsGenerator,
    }

    @classmethod
    def create_generator(
        cls,
        generator_type: str,
        project_root: Path,
        detected_languages: list[str],
        config: dict[str, Any],
    ) -> BaseGenerator:
        """
        指定されたタイプのジェネレーターを作成

        Args:
            generator_type: ジェネレーターのタイプ ('api', 'readme', 'agents')
            project_root: プロジェクトルートパス
            detected_languages: 検出された言語リスト
            config: 設定辞書

        Returns:
            ジェネレーターインスタンス
        """
        generator_class = cls._generators.get(generator_type)
        if generator_class is None:
            raise ValueError(f"Unknown generator type: {generator_type}")

        return generator_class(project_root, detected_languages, config)

    @classmethod
    def get_available_generators(cls) -> list[str]:
        """利用可能なジェネレーターのリストを取得"""
        return list(cls._generators.keys())
