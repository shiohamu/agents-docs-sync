#!/usr/bin/env python3
"""
汎用ドキュメント自動生成システム
コミット時にAPIドキュメントとREADME.mdを自動更新します。
"""

from pathlib import Path
import sys
from typing import Any

# プロジェクトルートのパスを取得
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCGEN_DIR = Path(__file__).parent.resolve()

# モジュールパスを追加（メインエントリーポイントとして実行される場合に必要）
# 注意: このファイルは直接実行されることを想定しているため、sys.path.insertが必要
# パッケージとしてインストールされた場合は相対インポートを使用
from .config_manager import ConfigManager
from .document_generator import DocumentGenerator
from .language_detector import LanguageDetector
from .utils.logger import get_logger

# ロガーの初期化
logger = get_logger("docgen")


class DocGen:
    """ドキュメント自動生成メインクラス"""

    def __init__(self, config_path: Path | None = None):
        """
        初期化

        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        self.project_root = PROJECT_ROOT
        self.docgen_dir = DOCGEN_DIR
        self.config_manager = ConfigManager(self.project_root, self.docgen_dir, config_path)
        self.language_detector = LanguageDetector(self.project_root)
        self.document_generator = None

    def get_config(self) -> dict[str, Any]:
        """現在の設定を取得"""
        return self.config_manager.get_config()

    def detect_languages(self, use_parallel: bool = True) -> list[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        return self.language_detector.detect_languages(use_parallel)

    def generate_documents(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        detected_languages = self.language_detector.get_detected_languages()
        if not detected_languages:
            detected_languages = self.detect_languages()

        if not detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        # DocumentGeneratorを初期化
        self.document_generator = DocumentGenerator(
            self.project_root, detected_languages, self.get_config()
        )

        return self.document_generator.generate_documents()


def main():
    """メインエントリーポイント"""
    import argparse

    try:
        from . import __version__
    except (ImportError, ValueError, SystemError):
        __version__ = "0.0.1"

    parser = argparse.ArgumentParser(description="汎用ドキュメント自動生成システム")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=Path, help="設定ファイルのパス")
    parser.add_argument("--detect-only", action="store_true", help="言語検出のみ実行")
    parser.add_argument("--no-api-doc", action="store_true", help="APIドキュメントを生成しない")
    parser.add_argument("--no-readme", action="store_true", help="READMEを更新しない")

    args = parser.parse_args()

    docgen = DocGen(config_path=args.config)

    if args.detect_only:
        languages = docgen.detect_languages()
        logger.info(f"\n検出された言語: {', '.join(languages) if languages else 'なし'}")
        return 0

    # 設定を一時的に上書き
    if args.no_api_doc:
        docgen.config_manager.update_config("generation.generate_api_doc", False)
    if args.no_readme:
        docgen.config_manager.update_config("generation.update_readme", False)

    if docgen.generate_documents():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
