"""
言語検出のベースクラス
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseDetector(ABC):
    """言語検出のベースクラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root

    @abstractmethod
    def detect(self) -> bool:
        """
        言語が使用されているか検出

        Returns:
            検出された場合True
        """
        pass

    @abstractmethod
    def get_language(self) -> str:
        """
        検出された言語名を返す

        Returns:
            言語名（例: 'python', 'javascript'）
        """
        pass

    def _file_exists(self, *paths) -> bool:
        """
        ファイルの存在を確認

        Args:
            *paths: 確認するファイルパス（相対パス）

        Returns:
            いずれかのファイルが存在する場合True
        """
        for path in paths:
            if (self.project_root / path).exists():
                return True
        return False

    def _has_files_with_ext(self, *extensions) -> bool:
        """
        指定された拡張子のファイルが存在するか確認

        Args:
            *extensions: 拡張子（例: '.py', '.js'）

        Returns:
            該当ファイルが存在する場合True
        """
        for ext in extensions:
            if list(self.project_root.rglob(f'*{ext}')):
                return True
        return False

