"""
ジェネレーターの基底クラス
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseGenerator(ABC):
    """ジェネレーターの基底クラス"""

    def __init__(
        self,
        project_root: Path,
        detected_languages: list[str],
        config: dict[str, Any],
        detected_package_managers: dict[str, str] | None = None,
    ):
        self.project_root = project_root
        self.detected_languages = detected_languages
        self.languages = detected_languages  # 後方互換性のため
        self.config = config
        self.detected_package_managers = detected_package_managers or {}

    @abstractmethod
    def generate(self) -> bool:
        """ドキュメントを生成"""
        pass
