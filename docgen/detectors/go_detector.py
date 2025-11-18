"""
Goプロジェクト検出モジュール
"""

from pathlib import Path
from .base_detector import BaseDetector


class GoDetector(BaseDetector):
    """Goプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        Goプロジェクトかどうかを検出

        Returns:
            Goプロジェクトの場合True
        """
        # go.mod, go.sum, Gopkg.toml などの存在確認
        if self._file_exists(
            'go.mod',
            'go.sum',
            'Gopkg.toml',
            'Gopkg.lock',
            'glide.yaml',
            'glide.lock'
        ):
            return True

        # .goファイルの存在確認
        if self._has_files_with_ext('.go'):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        return 'go'

