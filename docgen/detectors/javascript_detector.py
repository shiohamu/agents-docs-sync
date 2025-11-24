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
            if (self.project_root / source_dir).exists():
                if self._has_files_in_dir(source_dir, ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
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

    def _has_files_in_dir(self, directory: str, *extensions) -> bool:
        """
        特定ディレクトリ内のファイル存在確認

        Args:
            directory: ディレクトリ名
            *extensions: 拡張子

        Returns:
            該当ファイルが存在する場合True
        """
        dir_path = self.project_root / directory
        if not dir_path.exists():
            return False

        for ext in extensions:
            try:
                for file_path in dir_path.rglob(f"*{ext}"):
                    # 設定ファイルやテストファイルを除外
                    if self._is_likely_js_config_or_test(file_path):
                        continue
                    return True
            except (OSError, PermissionError):
                continue
        return False

    def _has_js_files_in_root(self) -> bool:
        """
        プロジェクトルート直下のJavaScriptファイル存在確認

        Returns:
            JavaScriptファイルが存在する場合True
        """
        for ext in [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"]:
            try:
                for file_path in self.project_root.glob(f"*{ext}"):
                    # 設定ファイルやテストファイルを除外
                    if self._is_likely_js_config_or_test(file_path):
                        continue
                    return True
            except (OSError, PermissionError):
                continue
        return False

    def _is_likely_js_config_or_test(self, file_path) -> bool:
        """
        設定ファイルやテストファイルか判定

        Args:
            file_path: ファイルパス

        Returns:
            設定ファイルやテストファイルの場合True
        """
        name = file_path.name.lower()

        # 設定ファイル
        config_patterns = [
            "webpack.config",
            "rollup.config",
            "vite.config",
            "babel.config",
            ".eslintrc",
            ".prettierrc",
            "jest.config",
            "vitest.config",
            "tsconfig",
            "jsconfig",
            "package-lock",
            "yarn.lock",
            "pnpm-lock",
        ]

        # テストファイル
        test_patterns = [
            ".test.",
            ".spec.",
            "test.",
            "spec.",
        ]

        # カバレッジやレポートファイル
        report_patterns = [
            "coverage",
            "htmlcov",
            ".coverage",
        ]

        # いずれかのパターンに一致する場合は除外
        return any(pattern in name for pattern in config_patterns + test_patterns + report_patterns)
