"""
Base Command

すべてのCLIコマンドの基底クラス
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseCommand(ABC):
    """CLIコマンドの基底クラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root

    @abstractmethod
    def execute(self, args: Any) -> int:
        """
        コマンドを実行

        Args:
            args: コマンドライン引数

        Returns:
            終了コード（0: 成功, 1: 失敗）
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        コマンド名を取得

        Returns:
            コマンド名
        """
        pass

    @abstractmethod
    def get_help(self) -> str:
        """
        ヘルプメッセージを取得

        Returns:
            ヘルプメッセージ
        """
        pass
