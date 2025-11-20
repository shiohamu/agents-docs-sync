"""
JavaScript/TypeScriptプロジェクト検出モジュール
"""

from .base_detector import BaseDetector


class JavaScriptDetector(BaseDetector):
    """JavaScript/TypeScriptプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        JavaScript/TypeScriptプロジェクトかどうかを検出

        Returns:
            JavaScript/TypeScriptプロジェクトの場合True
        """
        # package.json, yarn.lock, pnpm-lock.yaml などの存在確認
        if self._file_exists(
            "package.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "package-lock.json",
            "tsconfig.json",
            "jsconfig.json",
        ):
            return True

        # .js, .jsx, .ts, .tsxファイルの存在確認
        if self._has_files_with_ext(".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        # tsconfig.jsonがある場合はTypeScript
        if self._file_exists("tsconfig.json"):
            return "typescript"
        # TypeScriptファイルがあるか確認
        if self._has_files_with_ext(".ts", ".tsx"):
            return "typescript"
        return "javascript"
