"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
Outlines統合で構造化出力を実現
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

# 相対インポートを使用（docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
from ..models import AgentsDocument, ProjectInfo
from ..utils.logger import get_logger
from .base_generator import BaseGenerator

logger = get_logger("agents_generator")


class AgentsGenerator(BaseGenerator):
    """AGENTS.md生成クラス（OpenAI仕様準拠）"""

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

    def _get_output_path(self, config: dict[str, Any]) -> Path:
        output_path = Path(config.get("output", {}).get("agents_doc", "AGENTS.md"))
        if not output_path.is_absolute():
            output_path = self.project_root / output_path
        return output_path

    def _get_mode_key(self) -> str:
        return "agents_mode"

    def _get_document_type(self) -> str:
        return "AGENTS.md"

    def _get_structured_model(self):
        return AgentsDocument

    def _get_project_overview_section(self, content: str) -> str:
        return self._extract_description_section(content)

    def _extract_description_section(self, content: str) -> str:
        """
        Extract description section from content

        Args:
            content: README content

        Returns:
            Description section text
        """
        lines = content.split("\n")
        description_lines = []
        in_description = False

        for line in lines:
            if "<!-- MANUAL_START:description -->" in line:
                in_description = True
                continue
            elif "<!-- MANUAL_END:description -->" in line:
                break
            elif in_description:
                description_lines.append(line)

        return "\n".join(description_lines)

    def _create_llm_prompt(self, project_info: ProjectInfo) -> str:
        prompt = f"""以下のプロジェクト情報を基に、AIコーディングエージェント向けのAGENTS.mdドキュメントを生成してください。

{self._format_project_info_for_prompt(project_info)}

以下のセクションを含めてください:
1. プロジェクト概要（使用技術を含む）
2. 開発環境のセットアップ（前提条件、依存関係のインストール、LLM環境のセットアップ）
3. ビルドおよびテスト手順
4. コーディング規約
5. プルリクエストの手順

重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

        return prompt

    def _generate_template(self, project_info: ProjectInfo) -> str:
        """
        テンプレートベースでマークダウンを生成（既存の実装）

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        lines = []

        # ヘッダー
        lines.append("# AGENTS ドキュメント")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(
            "このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # プロジェクト概要
        lines.extend(self._generate_project_overview(project_info))
        lines.append("---")
        lines.append("")

        # 開発環境のセットアップ
        lines.extend(self._generate_setup_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # ビルドおよびテスト手順
        lines.extend(self._generate_build_test_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # コーディング規約
        lines.extend(self._generate_coding_standards_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # プルリクエストの手順
        lines.extend(self._generate_pr_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # カスタム指示
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            lines.extend(self._generate_custom_instructions_section(custom_instructions))
            lines.append("")
            lines.append("---")
            lines.append("")

        # フッター
        lines.append(
            f"*このドキュメントは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )
        lines.append("")

        return "\n".join(lines)

    def _generate_with_llm(self, project_info: ProjectInfo) -> str:
        """
        LLMを使用してAGENTS.mdを生成（Outlinesで構造化出力）

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列（エラー時はテンプレート生成にフォールバック）
        """
        try:
            # Outlinesを使用した構造化生成を試す
            if self._should_use_outlines():
                return self._generate_with_outlines(project_info)

            # 従来のLLM生成にフォールバック
            return self._generate_with_llm_legacy(project_info)

        except Exception as e:
            logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _generate_project_overview(self, project_info: ProjectInfo) -> list[str]:
        """プロジェクト概要セクションを生成"""
        lines = []
        lines.append("## プロジェクト概要")
        lines.append("")

        lines.append("<!-- MANUAL_START:description -->")
        lines.append("")

        # プロジェクト説明を取得
        from ..utils.markdown_utils import extract_project_description

        description = extract_project_description(self.project_root, project_info.description)
        lines.append(description)

        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        lines.append("")
        lines.append("<!-- MANUAL_END:description -->")
        return lines

    def _generate_setup_section(self, project_info: ProjectInfo) -> list[str]:
        """開発環境セットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        lines.append("### 前提条件")
        lines.append("")
        lines.append("- Python 3.12以上")
        if "javascript" in self.languages:
            lines.append("- Node.js 18以上")
        lines.append("")

        # 依存関係のインストール
        lines.append("### 依存関係のインストール")
        lines.append("")

        # Python依存関係
        if "python" in self.languages:
            pm = self.package_managers.get("python", "pip")
            lines.append("#### Python依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "uv":
                lines.append("uv sync")
            elif pm == "poetry":
                lines.append("poetry install")
            elif pm == "conda":
                lines.append("conda env create -f environment.yml")
            else:  # pip
                for dep_file in [
                    "requirements.txt",
                    "requirements-docgen.txt",
                    "requirements-test.txt",
                ]:
                    req_path = self.project_root / dep_file
                    if req_path.exists():
                        lines.append(f"pip install -r {dep_file}")
            lines.append("```")
            lines.append("")

        # JavaScript/TypeScript依存関係
        if "javascript" in self.languages or "typescript" in self.languages:
            pm = self.package_managers.get("javascript", "npm")
            lang_name = "TypeScript" if "typescript" in self.languages else "JavaScript"
            lines.append(f"#### {lang_name}依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "pnpm":
                lines.append("pnpm install")
            elif pm == "yarn":
                lines.append("yarn install")
            else:  # npm
                lines.append("npm install")
            lines.append("```")
            lines.append("")

        # Go依存関係
        if "go" in self.languages:
            pm = self.package_managers.get("go", "go")
            lines.append("#### Go依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "dep":
                lines.append("dep ensure")
            elif pm == "glide":
                lines.append("glide install")
            else:  # go modules
                lines.append("go mod download")
            lines.append("```")
            lines.append("")

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_llm_setup_section(self) -> list[str]:
        """LLM環境セットアップセクションを生成"""
        lines = []
        lines.append("### LLM環境のセットアップ")
        lines.append("")

        llm_mode = self.agents_config.get("llm_mode", "both")
        api_config = self.agents_config.get("api") or {}
        local_config = self.agents_config.get("local") or {}

        if llm_mode in ["api", "both"]:
            lines.append("#### APIを使用する場合")
            lines.append("")

            lines.append("1. **APIキーの取得と設定**")
            lines.append("")

            api_provider = api_config.get("provider", "openai")
            api_key_env = api_config.get("api_key_env", "OPENAI_API_KEY")

            if api_provider == "openai":
                lines.append("   - OpenAI APIキーを取得: https://platform.openai.com/api-keys")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            elif api_provider == "anthropic":
                lines.append("   - Anthropic APIキーを取得: https://console.anthropic.com/")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            else:
                api_endpoint = api_config.get("endpoint", "")
                lines.append(f"   - カスタムAPIエンドポイントを使用: {api_endpoint}")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")

            lines.append("")
            lines.append("2. **API使用時の注意事項**")
            lines.append("   - APIレート制限に注意してください")
            lines.append("   - コスト管理のために使用量を監視してください")
            lines.append("")

        if llm_mode in ["local", "both"]:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")

            lines.append("1. **ローカルLLMのインストール**")
            lines.append("")

            local_provider = local_config.get("provider", "ollama")
            local_model = local_config.get("model", "llama3")
            # 一般的な手順としてlocalhostを使用
            local_base_url = "http://localhost:11434"

            if local_provider == "ollama":
                lines.append("   - Ollamaをインストール: https://ollama.ai/")
                lines.append(f"   - モデルをダウンロード: `ollama pull {local_model}`")
                lines.append("   - サービスを起動: `ollama serve`")
                lines.append(f"   - ベースURL: {local_base_url}")
            elif local_provider == "lmstudio":
                lines.append("   - LM Studioをインストール: https://lmstudio.ai/")
                lines.append("   - モデルをダウンロードして起動")
                lines.append(f"   - ベースURL: {local_base_url}")
            else:
                lines.append("   - カスタムローカルLLMを設定")
                lines.append(f"   - ベースURL: {local_base_url}")

            lines.append("")
            lines.append("2. **ローカルLLM使用時の注意事項**")
            lines.append("   - モデルが起動していることを確認してください")
            lines.append("   - ローカルリソース（メモリ、CPU）を監視してください")
            lines.append("")

        return lines

    def _generate_build_test_section(self, project_info: ProjectInfo) -> list[str]:
        """ビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")

        # ビルド手順
        lines.append("### ビルド手順")
        lines.append("")
        build_commands = project_info.build_commands
        if build_commands:
            lines.append("```bash")
            for cmd in build_commands:
                lines.append(cmd)
            lines.append("```")
        else:
            lines.append("ビルド手順は設定されていません。")
        lines.append("")

        # テスト実行
        lines.append("### テスト実行")
        lines.append("")
        test_commands = project_info.test_commands
        if test_commands:
            llm_mode = self.agents_config.get("llm_mode", "both")

            if llm_mode in ["api", "both"]:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")

        return lines

    def _generate_coding_standards_section(self, project_info: ProjectInfo) -> list[str]:
        """コーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        coding_standards = project_info.coding_standards or {}

        if coding_standards:
            # フォーマッター
            formatter = coding_standards.get("formatter")
            if formatter:
                lines.append("### フォーマッター")
                lines.append("")
                lines.append(f"- **{formatter}** を使用")
                if formatter == "black":
                    lines.append("  ```bash")
                    lines.append("  black .")
                    lines.append("  ```")
                elif formatter == "prettier":
                    lines.append("  ```bash")
                    lines.append("  npx prettier --write .")
                    lines.append("  ```")
                lines.append("")

            # リンター
            linter = coding_standards.get("linter")
            if linter:
                lines.append("### リンター")
                lines.append("")
                lines.append(f"- **{linter}** を使用")
                if linter == "ruff":
                    lines.append("  ```bash")
                    lines.append("  ruff check .")
                    lines.append("  ruff format .")
                    lines.append("  ```")
                lines.append("")

            # スタイルガイド
            style_guide = coding_standards.get("style_guide")
            if style_guide:
                lines.append("### スタイルガイド")
                lines.append("")
                lines.append(f"- {style_guide} に準拠")
                lines.append("")
        else:
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_pr_section(self, project_info: ProjectInfo) -> list[str]:
        """プルリクエストセクションを生成"""
        lines = []
        lines.append("## プルリクエストの手順")
        lines.append("")
        lines.append("1. **ブランチの作成**")
        lines.append("   ```bash")
        lines.append("   git checkout -b feature/your-feature-name")
        lines.append("   ```")
        lines.append("")
        lines.append("2. **変更のコミット**")
        lines.append("   - コミットメッセージは明確で説明的に")
        lines.append("   - 関連するIssue番号を含める")
        lines.append("")
        lines.append("3. **テストの実行**")
        lines.append("   ```bash")
        test_commands = project_info.test_commands
        for cmd in test_commands:
            lines.append(f"   {cmd}")
        if not test_commands:
            lines.append("   # テストコマンドを実行")
        lines.append("   ```")
        lines.append("")
        lines.append("4. **プルリクエストの作成**")
        lines.append("   - タイトル: `[種類] 簡潔な説明`")
        lines.append("   - 説明: 変更内容、テスト結果、関連Issueを記載")
        lines.append("")

        return lines

    def _generate_custom_instructions_section(
        self, custom_instructions: str | dict[str, Any]
    ) -> list[str]:
        """カスタム指示セクションを生成"""
        lines = []
        lines.append("## プロジェクト固有の指示")
        lines.append("")

        if isinstance(custom_instructions, str):
            lines.append(custom_instructions)
        elif isinstance(custom_instructions, dict):
            # dictの場合はキーをセクションとして扱う
            for key, value in custom_instructions.items():
                lines.append(f"### {key}")
                lines.append("")
                lines.append(str(value))
                lines.append("")

        lines.append("")
        return lines

    def _convert_structured_data_to_markdown(
        self, data: AgentsDocument, project_info: ProjectInfo
    ) -> str:
        """
        構造化データをマークダウン形式に変換

        Args:
            data: 構造化されたAGENTSドキュメントデータ
            project_info: プロジェクト情報

        Returns:
            マークダウン形式の文字列
        """
        lines = []

        # ヘッダー
        lines.append(f"# {data.title}")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(
            "このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # プロジェクト概要
        lines.append("## プロジェクト概要")
        lines.append("")
        lines.append("<!-- MANUAL_START:description -->")
        lines.append("")
        lines.append(data.description)
        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        lines.append("")
        lines.append("<!-- MANUAL_END:description -->")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 開発環境のセットアップ
        lines.extend(
            self._generate_setup_section_from_structured(
                data.setup_instructions.model_dump() if data.setup_instructions else {}
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # ビルドおよびテスト手順
        lines.extend(
            self._generate_build_test_section_from_structured(
                data.build_test_instructions.model_dump() if data.build_test_instructions else {}
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # コーディング規約
        lines.extend(
            self._generate_coding_standards_from_structured(
                data.coding_standards.model_dump() if data.coding_standards else {}
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # プルリクエストの手順
        lines.extend(
            self._generate_pr_section_from_structured(
                data.pr_guidelines.model_dump() if data.pr_guidelines else {}
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # カスタム指示
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            lines.extend(self._generate_custom_instructions_section(custom_instructions))
            lines.append("")
            lines.append("---")
            lines.append("")

        # フッター
        lines.append(data.auto_generated_note)
        lines.append("")

        return "\n".join(lines)

    def _generate_setup_section_from_structured(self, setup_data: Any) -> list[str]:
        """構造化データからセットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        prerequisites = setup_data.get("prerequisites", [])
        if prerequisites:
            lines.append("### 前提条件")
            lines.append("")
            for prereq in prerequisites:
                lines.append(f"- {prereq}")
            lines.append("")

        # 依存関係のインストール
        installation_steps = setup_data.get("installation_steps", [])
        if installation_steps:
            lines.append("### 依存関係のインストール")
            lines.append("")
            lines.append("```bash")
            for step in installation_steps:
                lines.append(step)
            lines.append("```")
            lines.append("")

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_build_test_section_from_structured(self, build_test_data: Any) -> list[str]:
        """構造化データからビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")

        # ビルド手順
        build_commands = build_test_data.get("build_commands", [])
        if build_commands:
            lines.append("### ビルド手順")
            lines.append("")
            lines.append("```bash")
            for cmd in build_commands:
                # uvプロジェクトの場合はpythonコマンドにuv runをつける
                display_cmd = cmd
                if "python" in self.package_managers and self.package_managers["python"] == "uv":
                    if cmd.startswith("python") and not cmd.startswith("uv run"):
                        display_cmd = f"uv run {cmd}"
                lines.append(display_cmd)
            lines.append("```")
        else:
            lines.append("ビルド手順は設定されていません。")
        lines.append("")

        # テスト実行
        test_commands = build_test_data.get("test_commands", [])
        if test_commands:
            lines.append("### テスト実行")
            lines.append("")
            llm_mode = self.agents_config.get("llm_mode", "both")

            if llm_mode in ["api", "both"]:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    display_cmd = cmd
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if (
                            cmd.startswith("python") or cmd.startswith("pytest")
                        ) and not cmd.startswith("uv run"):
                            display_cmd = f"uv run {cmd}"
                    lines.append(display_cmd)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    display_cmd = cmd
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if (
                            cmd.startswith("python") or cmd.startswith("pytest")
                        ) and not cmd.startswith("uv run"):
                            display_cmd = f"uv run {cmd}"
                    lines.append(display_cmd)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")

        return lines

    def _generate_coding_standards_from_structured(self, standards_data: Any) -> list[str]:
        """構造化データからコーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        standards = standards_data.get("standards", [])
        if standards:
            for standard in standards:
                lines.append(f"- {standard}")
            lines.append("")
        else:
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_pr_section_from_structured(self, pr_data: Any) -> list[str]:
        """構造化データからプルリクエストセクションを生成"""
        lines = []
        lines.append("## プルリクエストの手順")
        lines.append("")

        branch_creation = pr_data.get("branch_creation", "ブランチを作成")
        lines.append("1. **ブランチの作成**")
        lines.append(f"   {branch_creation}")
        lines.append("")

        commit_guidelines = pr_data.get("commit_guidelines", "コミットメッセージは明確で説明的に")
        lines.append("2. **変更のコミット**")
        lines.append(f"   - {commit_guidelines}")
        lines.append("")

        lines.append("3. **テストの実行**")
        lines.append("   ```bash")
        lines.append("   # テストコマンドを実行")
        lines.append("   ```")
        lines.append("")

        pr_creation = pr_data.get("pr_creation", "プルリクエストを作成")
        lines.append("4. **プルリクエストの作成**")
        lines.append(f"   - {pr_creation}")
        lines.append("")

        return lines

    def _clean_llm_output(self, text: str) -> str:
        """
        LLMの出力から思考過程や試行錯誤の痕跡を削除

        Args:
            text: LLMで生成されたテキスト

        Returns:
            クリーンアップされたテキスト
        """
        from ..utils.markdown_utils import clean_llm_output_advanced

        return clean_llm_output_advanced(text)

    def _validate_output(self, text: str) -> bool:
        """
        LLMの出力を検証して、Pydanticモデルでパースできるかチェック

        Args:
            text: 検証するテキスト

        Returns:
            検証に合格したかどうか
        """
        if not text or not text.strip():
            return False

        try:
            # JSONとしてパースを試みる（LLM出力がJSON形式の場合）
            data = json.loads(text)
            AgentsDocument(**data)
            return True
        except (json.JSONDecodeError, ValidationError):
            # マークダウン形式の場合は基本的なチェックのみ
            text_lower = text.lower()

            # 特殊なマーカーパターンをチェック
            if (
                "<|channel|>" in text
                or "<|message|>" in text
                or "commentary/analysis" in text_lower
            ):
                logger.warning("特殊なマーカーパターンが検出されました")
                return False

            # 思考過程のパターンが含まれていないかチェック
            thinking_patterns = [
                "thus final answer",
                "let's generate",
                "but we need",
                "i will produce",
                "i think",
                "let's finalize",
                "we should produce",
                "we will output",
                "thus the final",
                "i'm going to",
                "let's output",
                "let's produce",
                "but i think it's",
                "thus final answer will be",
                "以下が、",
                "改訂版です",
                "we should now",
                "we will not include",
                "should we keep",
                "possibly they want",
                "but we must keep",
                "but we might need",
                "however, user wrote",
                "also note",
                "but the user",
                "ok final output",
                "ok. i'll generate",
                "let's create final output",
                "check that it doesn't",
                "now i will provide",
                "the user wants",
                "they gave",
                "so we should",
                "so we can",
                "also keep",
                "we must not include",
                "so final output",
                "but we must also keep",
                "we must only output",
                "but we must",
            ]

            for pattern in thinking_patterns:
                if pattern in text_lower:
                    logger.warning(f"思考過程のパターンが検出されました: {pattern}")
                    return False

            # プレースホルダーが含まれていないかチェック
            placeholder_patterns = [
                "???",
                "(??)",
                "... ...",
                "|  | |",
                "---‐‐‐",
                "# ... (continue)",
            ]

            for pattern in placeholder_patterns:
                if pattern in text:
                    logger.warning(f"プレースホルダーが検出されました: {pattern}")
                    return False

        # マークダウンコードブロック内に思考過程が含まれていないかチェック
        lines = text.split("\n")
        in_markdown_block = False
        for line in lines:
            if line.strip().startswith("```"):
                lang = line.strip()[3:].strip().lower()
                if "markdown" in lang:
                    in_markdown_block = True
                elif in_markdown_block:
                    in_markdown_block = False
            elif in_markdown_block:
                if any(pattern in line.lower() for pattern in thinking_patterns):
                    logger.warning("マークダウンコードブロック内に思考過程が検出されました")
                    return False

        return True
