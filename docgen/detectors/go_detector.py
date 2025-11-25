"""
Goプロジェクト検出モジュール
"""

from .base_detector import BaseDetector
from .detector_patterns import DetectorPatterns


class GoDetector(BaseDetector):
    """Goプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        Goプロジェクトかどうかを検出

        Returns:
            Goプロジェクトの場合True
        """
        # パッケージマネージャーファイルの存在確認
        if self._detect_by_package_files("go"):
            return True

        # .goファイルの存在確認
        if self._detect_by_extensions("go"):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        return "go"

    def detect_package_manager(self) -> str | None:
        """
        Goプロジェクトで使用されているパッケージマネージャを検出

        Returns:
            パッケージマネージャ名またはNone
        """
        return DetectorPatterns.detect_package_manager("go", self._file_exists)
