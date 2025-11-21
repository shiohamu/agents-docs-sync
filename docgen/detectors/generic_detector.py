"""
汎用言語検出モジュール
一般的なコメント形式をサポートする言語を検出
"""

from .base_detector import BaseDetector


class GenericDetector(BaseDetector):
    """汎用言語検出クラス"""

    # サポートする言語とその拡張子
    SUPPORTED_LANGUAGES = {
        "rust": [".rs"],
        "java": [".java"],
        "kotlin": [".kt", ".kts"],
        "scala": [".scala"],
        "ruby": [".rb"],
        "php": [".php"],
        "c": [".c", ".h"],
        "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".hxx"],
        "csharp": [".cs"],
        "swift": [".swift"],
        "dart": [".dart"],
        "r": [".r", ".R"],
        "lua": [".lua"],
        "perl": [".pl", ".pm"],
        "shell": [".sh", ".bash", ".zsh"],
        "powershell": [".ps1"],
    }

    def detect(self) -> bool:
        """
        サポートされている汎用言語が使用されているか検出

        Returns:
            サポート言語が検出された場合True
        """
        for _lang, extensions in self.SUPPORTED_LANGUAGES.items():
            if self._has_files_with_ext(*extensions):
                return True
        return False

    def get_language(self) -> str:
        """
        検出された言語名を返す
        複数検出された場合は最初に見つかったものを返す

        Returns:
            言語名
        """
        for lang, extensions in self.SUPPORTED_LANGUAGES.items():
            if self._has_files_with_ext(*extensions):
                return lang
        return "generic"

    def get_all_detected_languages(self) -> list:
        """
        検出されたすべての言語を返す

        Returns:
            検出された言語のリスト
        """
        detected = []
        for lang, extensions in self.SUPPORTED_LANGUAGES.items():
            if self._has_files_with_ext(*extensions):
                detected.append(lang)
        return detected

    def detect_package_manager(self) -> str | None:
        """
        汎用言語プロジェクトで使用されているパッケージマネージャを検出

        Returns:
            パッケージマネージャ名またはNone
        """
        # 汎用言語ではパッケージマネージャの検出は行わない
        return None
