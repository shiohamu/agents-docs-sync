"""
Pythonプロジェクト検出モジュール
"""

from .base_detector import BaseDetector
from .detector_patterns import DetectorPatterns


class PythonDetector(BaseDetector):
    """Pythonプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        Pythonプロジェクトかどうかを検出

        Returns:
            Pythonプロジェクトの場合True
        """
        # パッケージマネージャーファイルの存在確認
        if self._detect_by_package_files("python"):
            return True

        # .pyファイルの存在確認
        if self._detect_by_extensions("python"):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        return "python"

    def detect_package_manager(self) -> str | None:
        """
        Pythonプロジェクトで使用されているパッケージマネージャを検出

        Returns:
            パッケージマネージャ名またはNone
        """
        return DetectorPatterns.detect_python_package_manager(self.project_root)
