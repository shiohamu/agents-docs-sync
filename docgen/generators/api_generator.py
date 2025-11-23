"""
APIドキュメント生成モジュール
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..models import APIInfo
from .parsers.generic_parser import GenericParser
from .parsers.js_parser import JSParser
from .parsers.python_parser import PythonParser

if TYPE_CHECKING:
    from .parsers.base_parser import BaseParser

# ロガーのインポート
from ..base_generator import BaseGenerator
from ..generators.parsers.base_parser import BaseParser
from ..utils.cache import CacheManager
from ..utils.logger import get_logger

logger = get_logger("api_generator")


class APIGenerator(BaseGenerator):
    """APIドキュメント生成クラス"""

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
            package_managers: 検出されたパッケージマネージャの辞書
        """
        super().__init__(project_root, languages, config, package_managers)
        self.output_path = Path(config.get("output", {}).get("api_doc", "docs/api.md"))
        if not self.output_path.is_absolute():
            self.output_path = project_root / self.output_path

        # キャッシュマネージャーの初期化
        cache_enabled = config.get("cache", {}).get("enabled", True)
        self.cache_manager = (
            CacheManager(project_root=project_root, enabled=cache_enabled)
            if cache_enabled
            else None
        )

    def generate(self) -> bool:
        """
        APIドキュメントを生成

        Returns:
            成功したかどうか
        """
        try:
            # 出力ディレクトリを作成
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            # 各言語のパーサーでAPI情報を収集
            all_apis = []
            parsers = self._get_parsers()

            # 除外ディレクトリとファイルパターンを設定
            exclude_dirs = self.config.get("exclude", {}).get(
                "directories",
                [
                    ".git",
                    "docgen",
                    "__pycache__",
                    "node_modules",
                    ".venv",
                    "venv",
                    "htmlcov",
                    ".pytest_cache",
                    "dist",
                    "build",
                ],
            )

            # キャッシュの使用設定
            use_cache = self.config.get("cache", {}).get("enabled", True)

            for parser in parsers:
                apis = parser.parse_project(
                    exclude_dirs=exclude_dirs,
                    use_cache=use_cache,
                    cache_manager=self.cache_manager,
                )
                all_apis.extend(apis)

            # API情報をソート（ファイル名、行番号順）
            all_apis.sort(key=lambda x: (x["file"], x["line"]))

            # マークダウンを生成
            markdown = self._generate_markdown(all_apis)

            # ファイルに書き込み
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            return True
        except Exception as e:
            logger.error(
                f"APIドキュメント生成中に予期しないエラーが発生しました: {e}", exc_info=True
            )
            return False

    def _get_parsers(self) -> list["BaseParser"]:
        """
        言語に応じたパーサーのリストを取得

        Returns:
            パーサーのリスト
        """
        parsers = []

        for lang in self.languages:
            if lang == "python":
                parsers.append(PythonParser(self.project_root))
            elif lang in ["javascript", "typescript"]:
                parsers.append(JSParser(self.project_root))
            else:
                parsers.append(GenericParser(self.project_root, language=lang))

        return parsers

    def _generate_markdown(self, apis: list[APIInfo]) -> str:
        """
        API情報からマークダウンを生成

        Args:
            apis: API情報のリスト

        Returns:
            マークダウンの文字列
        """
        lines = []

        # ヘッダー
        lines.append("# API ドキュメント")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        if not apis:
            lines.append("APIが見つかりませんでした。")
            return "\n".join(lines)

        # ファイルごとにグループ化
        current_file = None
        for api in apis:
            file_path = api["file"]

            # 新しいファイルセクション
            if file_path != current_file:
                if current_file is not None:
                    lines.append("")
                current_file = file_path
                lines.append(f"## {file_path}")
                lines.append("")

            # API情報を出力
            lines.append(f"### {api['name']}")
            lines.append("")
            lines.append(f"**型**: `{api['type']}`")
            lines.append("")
            lines.append("**シグネチャ**:")
            lines.append("```")
            lines.append(api["signature"])
            lines.append("```")
            lines.append("")

            if api["docstring"]:
                lines.append("**説明**:")
                lines.append("")
                # docstringを整形（インデントを調整）
                docstring_lines = api["docstring"].split("\n")
                for doc_line in docstring_lines:
                    lines.append(doc_line)
                lines.append("")
            else:
                lines.append("*説明なし*")
                lines.append("")

            lines.append(f"*定義場所: {file_path}:{api['line']}*")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
