#!/usr/bin/env python3
"""
汎用ドキュメント自動生成システム
コミット時にAPIドキュメントとREADME.mdを自動更新します。
"""

from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

# プロジェクトルートのパスを取得
DOCGEN_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = DOCGEN_DIR.parent

# sys.pathにプロジェクトルートを追加（パッケージとして実行する場合）
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# パッケージとしてインストールされた場合は相対インポートを使用
from .config_manager import ConfigManager
from .document_generator import DocumentGenerator
from .language_detector import LanguageDetector
from .utils.exceptions import ErrorMessages
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
            self.project_root, self.docgen_dir, self.config_path, package_config_sample
        )
        self.config = self.config_manager.get_config()
        self.language_detector = LanguageDetector(self.project_root)
        self.detected_languages = []
        self.detected_package_managers = {}

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
        self.detect_languages()

        if not self.detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        document_generator = DocumentGenerator(
            self.project_root, self.detected_languages, self.config, self.detected_package_managers
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

        subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

        # commit-msg サブコマンド
        subparsers.add_parser("commit-msg", help="コミットメッセージ生成")

        # hooks サブコマンド
        hooks_parser = subparsers.add_parser("hooks", help="Git hooksの管理")
        hooks_parser.add_argument(
            "action", choices=["enable", "disable"], help="hooksを有効化または無効化"
        )

        # init サブコマンド
        init_parser = subparsers.add_parser(
            "init", help="プロジェクトの初期化（必須ファイルを作成）"
        )
        init_parser.add_argument("--force", action="store_true", help="既存ファイルを強制上書き")

        args = parser.parse_args()

        # 実行時のカレントディレクトリをプロジェクトルートとして使用
        project_root = Path.cwd().resolve()

        # init コマンド（DocGen初期化前に処理）
        if args.command == "init":
            return self._handle_init(args.force, project_root)

        # DocGenの初期化（config.yamlが必要）
        # 必須ファイルがない場合は自動初期化
        if args.command not in ["init"]:
            auto_init_result = self._check_and_auto_init(project_root)
            if auto_init_result != 0:
                return auto_init_result

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
            logger.error(ErrorMessages.HOOKS_DIR_NOT_FOUND)
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
                logger.warning(
                    ErrorMessages.HOOK_SOURCE_NOT_FOUND.format(
                        hook_name=hook_name, source_file=source_file
                    )
                )
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
                    with open(source_file) as src:
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
            with open(hook_file) as f:
                return "# docgen" in f.read()
        except FileNotFoundError:
            return False

    def _has_shebang(self, hook_file):
        """フックファイルにシェバンがあるかどうかをチェック"""
        try:
            with open(hook_file) as f:
                first_line = f.readline().strip()
                return first_line.startswith("#!")
        except FileNotFoundError:
            return False

    def _handle_init(self, force: bool, project_root: Path, quiet: bool = False) -> int:
        """プロジェクトの初期化処理

        Args:
            force: 既存ファイルを強制上書き
            project_root: プロジェクトルート
            quiet: 詳細メッセージを抑制（自動初期化時に使用）

        Returns:
            成功時は0、失敗時は1
        """
        docgen_dir = project_root / "docgen"
        config_file = docgen_dir / "config.yaml"

        # 既存ファイルチェック
        if config_file.exists() and not force:
            logger.warning(
                f"設定ファイルが既に存在します: {config_file}\n"
                "上書きする場合は --force フラグを使用してください。"
            )
            return 1

        # docgenディレクトリの作成
        docgen_dir.mkdir(parents=True, exist_ok=True)

        # パッケージ内のソースディレクトリ（インストールされたパッケージまたは開発モード）
        package_docgen_dir = DOCGEN_DIR

        try:
            # 1. config.yaml.sampleをconfig.yamlにコピー
            source_config = package_docgen_dir / "config.yaml.sample"
            if source_config.exists():
                shutil.copy2(source_config, config_file)
                if not quiet:
                    logger.info(f"✓ 設定ファイルを作成しました: {config_file}")
            else:
                logger.error(f"ソースファイルが見つかりません: {source_config}")
                return 1

            # 2. templatesディレクトリのコピー
            self._copy_directory_contents(
                package_docgen_dir / "templates",
                docgen_dir / "templates",
                quiet=quiet,
                description="テンプレート",
            )

            # 3. promptsディレクトリのコピー
            self._copy_directory_contents(
                package_docgen_dir / "prompts",
                docgen_dir / "prompts",
                quiet=quiet,
                description="プロンプト",
            )

            # 4. hooksディレクトリのコピー（実行権限付与）
            hooks_copied = self._copy_directory_contents(
                package_docgen_dir / "hooks",
                docgen_dir / "hooks",
                quiet=quiet,
                description="Git hooks",
            )

            # hooksファイルに実行権限を付与
            if hooks_copied:
                hooks_dir = docgen_dir / "hooks"
                for hook_file in hooks_dir.iterdir():
                    if hook_file.is_file():
                        hook_file.chmod(0o755)

            if not quiet:
                logger.info("✓ プロジェクトの初期化が完了しました")

            return 0

        except Exception as e:
            logger.error(f"初期化中にエラーが発生しました: {e}")
            return 1

    def _copy_directory_contents(
        self, source_dir: Path, dest_dir: Path, quiet: bool = False, description: str = "ファイル"
    ) -> bool:
        """ディレクトリの内容をコピー

        Args:
            source_dir: コピー元ディレクトリ
            dest_dir: コピー先ディレクトリ
            quiet: 詳細メッセージを抑制
            description: ログ用の説明文

        Returns:
            成功時はTrue、失敗時はFalse
        """
        if not source_dir.exists():
            logger.warning(f"ソースディレクトリが見つかりません: {source_dir}")
            return False

        dest_dir.mkdir(parents=True, exist_ok=True)

        try:
            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, dest_dir / item.name)

            if not quiet:
                file_count = len(list(dest_dir.iterdir()))
                logger.info(f"✓ {description}をコピーしました: {file_count}ファイル")

            return True

        except Exception as e:
            logger.error(f"{description}のコピー中にエラーが発生しました: {e}")
            return False

    def _check_and_auto_init(self, project_root: Path) -> int:
        """必須ファイルがない場合に自動初期化

        Args:
            project_root: プロジェクトルート

        Returns:
            成功時は0、失敗時は1
        """
        config_path = project_root / "docgen" / "config.yaml"

        if not config_path.exists():
            logger.info("必須ファイルが見つかりません。初期化を実行します...")
            result = self._handle_init(force=True, project_root=project_root, quiet=True)
            if result == 0:
                logger.info("✓ 初期化が完了しました")
            return result

        return 0


def main():
    """メインエントリーポイント"""
    try:
        cli = CommandLineInterface()
        sys.exit(cli.run())
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
