"""
JavaScript/TypeScriptプロジェクト検出モジュール
"""

from .base_detector import BaseDetector
from .detector_patterns import DetectorPatterns


class JavaScriptDetector(BaseDetector):
    """JavaScript/TypeScriptプロジェクト検出クラス"""

    def detect(self) -> bool:
        """
        JavaScript/TypeScriptプロジェクトかどうかを検出

        Returns:
            JavaScript/TypeScriptプロジェクトの場合True
        """
        # package.jsonの存在確認（最も確実な指標）
        if self._file_exists("package.json"):
            return True

        # tsconfig.json, jsconfig.jsonの存在確認
        if self._file_exists("tsconfig.json", "jsconfig.json"):
            return True

        # yarn.lock, pnpm-lock.yaml, package-lock.jsonの存在確認
        if self._file_exists("yarn.lock", "pnpm-lock.yaml", "package-lock.json"):
            return True

        # ソースディレクトリ内の.js, .jsx, .ts, .tsxファイルの存在確認
        # ソースディレクトリを優先的にチェック
        source_dirs = ["src", "lib", "app", "components"]
        for source_dir in source_dirs:
            if self._has_files_in_dir(
                source_dir, ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", exclude_config=True
            ):
                return True

        # プロジェクトルート直下のJavaScriptファイル（ただし設定ファイルは除外）
        if self._has_js_files_in_root():
            return True

        return False

    def get_language(self) -> str:
        """言語名を返す"""
        # まずJavaScriptプロジェクトとして検出されているか確認
        if not self.detect():
            return "unknown"

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
        return DetectorPatterns.detect_package_manager("javascript", self._file_exists)

    def _has_js_files_in_root(self) -> bool:
        """
        プロジェクトルート直下のJavaScriptファイル存在確認

        Returns:
            JavaScriptファイルが存在する場合True
        """
        return self._has_files_in_root(
            ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", exclude_config=True
        )

    def _is_likely_js_config_or_test(self, file_path) -> bool:
        """
        設定ファイルやテストファイルか判定

        Args:
            file_path: ファイルパス

        Returns:
            設定ファイルやテストファイルの場合True
        """
        return DetectorPatterns.is_js_config_or_test(file_path)
