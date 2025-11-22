"""
コマンドラインインターフェースモジュール
"""

from pathlib import Path
import sys
import os
import shutil
import subprocess

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

        subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

        # commit-msg サブコマンド
        subparsers.add_parser("commit-msg", help="コミットメッセージ生成")

        # hooks サブコマンド
        hooks_parser = subparsers.add_parser("hooks", help="Git hooksの管理")
        hooks_parser.add_argument(
            "action", choices=["enable", "disable"], help="hooksを有効化または無効化"
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

        # hooks コマンド
        if args.command == "hooks":
            return self._handle_hooks(args.action, project_root)

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

    def _handle_hooks(self, action, project_root):
        """Git hooksの有効化/無効化を処理"""
        git_hooks_dir = project_root / ".git" / "hooks"
        docgen_hooks_dir = project_root / "docgen" / "hooks"

        if not docgen_hooks_dir.exists():
            logger.error("docgen/hooks ディレクトリが見つかりません")
            return 1

        hook_names = ["pre-commit", "post-commit", "pre-push", "commit-msg"]

        if action == "enable":
            return self._enable_hooks(git_hooks_dir, docgen_hooks_dir, hook_names)
        elif action == "disable":
            return self._disable_hooks(git_hooks_dir, hook_names)
        else:
            logger.error(f"不明なアクション: {action}")
            return 1

    def _enable_hooks(self, git_hooks_dir, docgen_hooks_dir, hook_names):
        """hooksを有効化"""
        git_hooks_dir.mkdir(parents=True, exist_ok=True)

        for hook_name in hook_names:
            source_file = docgen_hooks_dir / hook_name
            hook_file = git_hooks_dir / hook_name

            if not source_file.exists():
                logger.warning(f"{hook_name} のソースファイルが見つかりません: {source_file}")
                continue

            # 既存のフックをバックアップ
            if hook_file.exists() and not self._is_docgen_hook(hook_file):
                backup_file = hook_file.with_suffix(
                    f"{hook_file.suffix}.backup.{subprocess.run(['date', '+%Y%m%d_%H%M%S'], capture_output=True, text=True).stdout.strip()}"
                )
                shutil.copy2(hook_file, backup_file)
                logger.info(f"既存の{hook_name}フックをバックアップしました: {backup_file}")

            # フックを追加
            if not self._is_docgen_hook(hook_file):
                with open(hook_file, "a") as f:
                    if not hook_file.exists() or not self._has_shebang(hook_file):
                        f.write("#!/bin/bash\n")
                    f.write(f"\n# docgen - {hook_name} hook\n")
                    with open(source_file, "r") as src:
                        f.write(src.read())
                hook_file.chmod(0o755)
                logger.info(f"✓ {hook_name}フックをインストールしました")
            else:
                logger.info(f"✓ {hook_name}フックは既にインストールされています")

        logger.info("Gitフックを有効化しました")
        return 0

    def _disable_hooks(self, git_hooks_dir, hook_names):
        """hooksを無効化"""
        for hook_name in hook_names:
            hook_file = git_hooks_dir / hook_name
            disabled_file = hook_file.with_suffix(f"{hook_file.suffix}.disabled")

            if hook_file.exists():
                if self._is_docgen_hook(hook_file):
                    shutil.move(hook_file, disabled_file)
                    logger.info(f"✓ {hook_name}フックを無効化しました")
                else:
                    logger.info(f"✓ {hook_name}フックはdocgenフックではありません（無視）")
            else:
                logger.info(f"✓ {hook_name}フックは存在しません")

        logger.info("Gitフックを無効化しました")
        return 0

    def _is_docgen_hook(self, hook_file):
        """フックファイルがdocgenフックかどうかをチェック"""
        try:
            with open(hook_file, "r") as f:
                return "# docgen" in f.read()
        except FileNotFoundError:
            return False

    def _has_shebang(self, hook_file):
        """フックファイルにシェバンがあるかどうかをチェック"""
        try:
            with open(hook_file, "r") as f:
                first_line = f.readline().strip()
                return first_line.startswith("#!")
        except FileNotFoundError:
            return False


def main():
    """メインエントリーポイント"""
    try:
        cli = CommandLineInterface()
        sys.exit(cli.run())
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
