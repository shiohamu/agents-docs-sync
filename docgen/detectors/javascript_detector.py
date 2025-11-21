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

    def detect_package_manager(self) -> str | None:
        """
        JavaScript/TypeScriptプロジェクトで使用されているパッケージマネージャを検出

        Returns:
            パッケージマネージャ名またはNone
        """
        # pnpm-lock.yamlが存在する場合（優先度最高）
        if self._file_exists("pnpm-lock.yaml"):
            return "pnpm"

        # yarn.lockが存在する場合
        if self._file_exists("yarn.lock"):
            return "yarn"

        # package-lock.jsonが存在する場合
        if self._file_exists("package-lock.json"):
            return "npm"

        # package.jsonが存在する場合（デフォルトnpm）
        if self._file_exists("package.json"):
            return "npm"

        return None
