"""
コミットメッセージ生成モジュール
LLMを使用してGitのコミットメッセージを自動生成
"""

from pathlib import Path
import subprocess
from typing import Any

try:
    from ..utils.llm_client import LLMClientFactory
    from ..utils.logger import get_logger
except ImportError:
    import sys

    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from utils.llm_client import LLMClientFactory
    from utils.logger import get_logger

logger = get_logger("commit_message_generator")


class CommitMessageGenerator:
    """コミットメッセージ生成クラス"""

    def __init__(self, project_root: Path, config: dict[str, Any]):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            config: 設定辞書
        """
        self.project_root = project_root
        self.config = config
        self.agents_config = config.get("agents", {})

    def generate(self) -> str | None:
        """
        コミットメッセージを生成

        Returns:
            生成されたコミットメッセージ（エラー時はNone）
        """
        try:
            # ステージング済みの変更を取得
            staged_changes = self._get_staged_changes()

            if not staged_changes:
                logger.warning("ステージング済みの変更がありません。")
                return None

            # LLMクライアントを取得
            llm_mode = self.agents_config.get("llm_mode", "api")
            preferred_mode = "api" if llm_mode in ["api", "both"] else "local"

            client = LLMClientFactory.create_client_with_fallback(
                self.agents_config, preferred_mode=preferred_mode
            )

            if not client:
                logger.warning("LLMクライアントの作成に失敗しました。")
                return None

            # プロンプトを作成
            prompt = self._create_prompt(staged_changes)

            # システムプロンプト
            system_prompt = """あなたはGitコミットメッセージ作成の専門家です。
変更内容を分析して、適切なコミットメッセージを生成してください。
Conventional Commits形式（例: feat: 機能追加、fix: バグ修正、docs: ドキュメント更新）を推奨しますが、必須ではありません。
簡潔で明確なメッセージを1行で生成してください。"""

            # LLMで生成
            logger.info("LLMを使用してコミットメッセージを生成中...")
            generated_message = client.generate(prompt, system_prompt=system_prompt)

            if generated_message:
                # 生成されたメッセージをクリーンアップ（改行を削除、先頭・末尾の空白を削除）
                message = generated_message.strip().split("\n")[0].strip()
                return message
            else:
                logger.warning("LLM生成が空でした。")
                return None

        except Exception as e:
            logger.error(f"コミットメッセージ生成中にエラーが発生しました: {e}", exc_info=True)
            return None

    def _get_staged_changes(self) -> str | None:
        """
        ステージング済みの変更を取得

        Returns:
            git diff --cachedの出力（エラー時はNone）
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                logger.warning(f"git diff --cachedが失敗しました: {result.stderr}")
                return None

            # 統計情報とdiffの両方を取得
            stat_output = result.stdout

            # 詳細なdiffも取得
            diff_result = subprocess.run(
                ["git", "diff", "--cached"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            if diff_result.returncode == 0:
                # diffが長すぎる場合は最初の部分のみ
                diff_output = diff_result.stdout
                if len(diff_output) > 5000:
                    diff_output = diff_output[:5000] + "\n... (truncated)"
                return f"{stat_output}\n\n{diff_output}"
            else:
                return stat_output

        except FileNotFoundError:
            logger.error("gitコマンドが見つかりません。")
            return None
        except Exception as e:
            logger.error(f"ステージング済みの変更の取得中にエラーが発生しました: {e}")
            return None

    def _create_prompt(self, staged_changes: str) -> str:
        """
        LLM用のプロンプトを作成

        Args:
            staged_changes: ステージング済みの変更内容

        Returns:
            プロンプト文字列
        """
        prompt = f"""以下のGitの変更内容を分析して、適切なコミットメッセージを生成してください。

変更内容:
{staged_changes}

上記の変更を要約したコミットメッセージを1行で生成してください。
Conventional Commits形式（例: feat: 機能追加、fix: バグ修正、docs: ドキュメント更新、refactor: リファクタリング）を推奨します。
簡潔で明確なメッセージにしてください。"""

        return prompt
