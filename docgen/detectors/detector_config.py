"""
検出設定のデータクラス定義
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PackageManagerRule:
    """パッケージマネージャ検出ルール"""

    files: tuple[str, ...]  # 必要なファイル（全て存在する必要）
    manager: str  # パッケージマネージャ名
    priority: int = 5  # 優先度（高いほど優先）
    needs_content_check: bool = False  # ファイル内容のチェックが必要か

    def __post_init__(self):
        """バリデーション"""
        if not self.files:
            raise ValueError("files must not be empty")
        if not self.manager:
            raise ValueError("manager must not be empty")
        if self.priority < 0:
            raise ValueError("priority must be non-negative")


@dataclass(frozen=True)
class LanguageConfig:
    """言語検出設定"""

    name: str  # 言語名
    extensions: tuple[str, ...] = field(default_factory=tuple)  # ソースファイル拡張子
    package_files: tuple[str, ...] = field(default_factory=tuple)  # パッケージ管理ファイル
    package_manager_rules: tuple[PackageManagerRule, ...] = field(
        default_factory=tuple
    )  # パッケージマネージャ検出ルール

    # 特殊検出ロジック（オプション）
    custom_detector: Callable[[Path], bool] | None = None
    custom_package_manager_detector: Callable[[Path], str | None] | None = None

    def __post_init__(self):
        """バリデーション"""
        if not self.name:
            raise ValueError("name must not be empty")

    def get_sorted_package_manager_rules(self) -> list[PackageManagerRule]:
        """優先度順にソートされたパッケージマネージャルールを返す"""
        return sorted(self.package_manager_rules, key=lambda r: r.priority, reverse=True)
