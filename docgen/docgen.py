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
sys.path.insert(0, str(PROJECT_ROOT))

from .config_manager import ConfigManager
from .document_generator import DocumentGenerator
from .language_detector import LanguageDetector
from .utils.logger import get_logger

# ロガーの初期化
logger = get_logger("docgen")


class DocGen:
    """ドキュメント自動生成メインクラス"""

    def __init__(self, project_root: Path | None = None, config_path: Path | None = None):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ（Noneの場合は現在の作業ディレクトリ）
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        # プロジェクトルートの決定
        # パッケージとしてインストールされた場合、実行時のカレントディレクトリを使用
        if project_root is None:
            self.project_root = Path.cwd().resolve()
        else:
            if not project_root or str(project_root) == ".":
                raise ValueError("プロジェクトルートが無効です")
            resolved_root = Path(project_root).resolve()
            self.project_root = resolved_root

        # docgenディレクトリはプロジェクトルート内のdocgenディレクトリ
        self.docgen_dir = self.project_root / "docgen"

        # パッケージ内のconfig.yaml.sampleを参照するためのパス
        package_config_sample = DOCGEN_DIR / "config.yaml.sample"

        self.config_path = config_path or self.docgen_dir / "config.yaml"

        self.config_manager = ConfigManager(
            self.project_root, self.docgen_dir, config_path, package_config_sample
        )
        self.config = self.config_manager.get_config()
        self.language_detector = LanguageDetector(self.project_root)
        self.detected_languages = []
        self.detected_package_managers = {}

    def _load_config(self):
        return self.config_manager._load_config()

    def _validate_config(self):
        self.config_manager._validate_config()
        self.config = self.config_manager.config

    def detect_languages(self, use_parallel: bool = True) -> list[str]:
        """
        プロジェクトの使用言語を自動検出

        Args:
            use_parallel: 並列処理を使用するかどうか（デフォルト: True）

        Returns:
            検出された言語のリスト
        """
        self.detected_languages = self.language_detector.detect_languages(use_parallel)
        self.detected_package_managers = self.language_detector.detected_package_managers
        return self.detected_languages

    def update_config(self, updates: dict[str, Any]) -> None:
        """
        設定を動的に更新

        Args:
            updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）
        """
        self.config_manager.update_config(updates)
        self.config = self.config_manager.get_config()

    def generate_documents(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        detected_languages = self.language_detector.get_detected_languages()
        if not detected_languages:
            self.detect_languages()
            detected_languages = self.language_detector.get_detected_languages()

        if not detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        detected_package_managers = self.language_detector.get_detected_package_managers()
        document_generator = DocumentGenerator(
            self.project_root, detected_languages, self.config, detected_package_managers
        )
        return document_generator.generate_documents()


class CommandLineInterface:
    """コマンドラインインターフェースクラス"""

    def __init__(self):
        self.docgen = None

    def run(self) -> int:
        """メイン実行メソッド"""
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
        parser.add_argument(
            "command",
            nargs="?",
            choices=["commit-msg"],
            help="実行するコマンド（commit-msg: コミットメッセージ生成）",
        )

        args = parser.parse_args()

        # 実行時のカレントディレクトリをプロジェクトルートとして使用
        project_root = Path.cwd().resolve()
        self.docgen = DocGen(project_root=project_root, config_path=args.config)

        # コミットメッセージ生成コマンド
        if args.command == "commit-msg":
            try:
                from .generators.commit_message_generator import CommitMessageGenerator
            except (ImportError, ValueError, SystemError):
                from generators.commit_message_generator import CommitMessageGenerator

            generator = CommitMessageGenerator(project_root, self.docgen.config)
            message = generator.generate()
            if message:
                print(message)
                return 0
            else:
                return 1

        if args.detect_only:
            languages = self.docgen.detect_languages()
            logger.info(f"\n検出された言語: {', '.join(languages) if languages else 'なし'}")
            return 0

        # 設定を一時的に上書き
        if args.no_api_doc:
            self.docgen.config_manager.update_config({"generation.generate_api_doc": False})
        if args.no_readme:
            self.docgen.config_manager.update_config({"generation.update_readme": False})

        if self.docgen.generate_documents():
            return 0
        else:
            return 1


def main():
    """メインエントリーポイント"""
    cli = CommandLineInterface()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
