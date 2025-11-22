"""
コマンドラインインターフェースモジュール
"""

from pathlib import Path
import sys

from .docgen import DocGen
from .utils.logger import get_logger

logger = get_logger("cli")


class CommandLineInterface:
    """コマンドラインインターフェースクラス"""

    def __init__(self):
        self.docgen = None

    def run(self):
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
