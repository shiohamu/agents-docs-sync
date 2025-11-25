"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
Outlines統合で構造化出力を実現
"""

from pathlib import Path
from typing import Any

# 相対インポートを使用（docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
from ..models.agents import AgentsDocument
from ..models.project import ProjectInfo
from ..utils.markdown_utils import (
    DESCRIPTION_END,
    DESCRIPTION_START,
    OTHER_END,
    OTHER_START,
    SETUP_END,
    SETUP_START,
    UNKNOWN,
    USAGE_END,
    USAGE_START,
    format_commands_with_package_manager,
    get_current_timestamp,
)
from .base_generator import BaseGenerator


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

    @property
    def agents_path(self):
        return self.output_path

    def _get_mode_key(self) -> str:
        return "agents_mode"

    def _get_output_key(self) -> str:
        return "agents_doc"

    def _get_document_type(self) -> str:
        return "AGENTS.md"

    def _get_structured_model(self):
        return AgentsDocument

    def _get_project_overview_section(self, content: str) -> str:
        return self._extract_description_section(content)

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
        Jinja2テンプレートを使用してAGENTS.mdを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # Extract manual sections from existing AGENTS.md
        try:
            existing_content = self.agents_path.read_text()
            manual_sections = self._extract_manual_sections(existing_content)
        except (FileNotFoundError, OSError):
            manual_sections = {}

        # コンテキストの準備
        context = {
            "timestamp": get_current_timestamp(),
            "description": self._generate_project_overview_content(project_info, manual_sections),
            "languages": self.languages,
            "javascript": "javascript" in self.languages,
            "go": "go" in self.languages,
            "installation_steps": "\n".join(self._generate_installation_section()),
            "llm_setup": "\n".join(self._generate_llm_setup_section()),
            "build_commands": self._generate_build_commands_content(project_info),
            "test_commands": self._generate_test_commands_content(project_info),
            "coding_standards": "\n".join(self._generate_coding_standards_section(project_info)),
            "pr_guidelines": "\n".join(self._generate_pr_section(project_info)),
            "custom_instructions": self._generate_custom_instructions_content(),
        }

        # Jinja2テンプレートでレンダリング
        return self._render_template("agents_template.md.j2", context)

    def _generate_project_overview_section(
        self, project_info: ProjectInfo, manual_sections: dict[str, str]
    ) -> str:
        """プロジェクト概要セクションを生成"""
        description = self._generate_project_overview_content(project_info, manual_sections)
        languages_str = ", ".join(self.languages) if self.languages else UNKNOWN
        return f"""## プロジェクト概要

<!-- MANUAL_START:description -->
{description}
<!-- MANUAL_END:description -->

**使用技術**: {languages_str}

---
"""

    def _generate_setup_section_full(self, project_info: ProjectInfo) -> str:
        """セットアップセクション全体を生成"""
        js_line = "\n- Node.js 18以上" if "javascript" in self.languages else ""
        return f"""## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
### 前提条件

- Python 3.12以上{js_line}

### 依存関係のインストール

{self._generate_installation_steps()}

### LLM環境のセットアップ

{self._generate_llm_setup_content()}
<!-- MANUAL_END:setup -->

---
"""

    def _generate_build_test_section_full(self, project_info: ProjectInfo) -> str:
        """ビルド/テストセクション全体を生成"""
        return f"""## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順

{self._generate_build_commands_content(project_info)}

### テスト実行

{self._generate_test_commands_content(project_info)}
<!-- MANUAL_END:usage -->

---
"""

    def _generate_coding_standards_section_full(self, project_info: ProjectInfo) -> str:
        """コーディング規約セクション全体を生成"""
        return f"""## コーディング規約

<!-- MANUAL_START:other -->
{self._generate_coding_standards_content(project_info)}
<!-- MANUAL_END:other -->

---
"""

    def _generate_pr_section_full(self, project_info: ProjectInfo) -> str:
        """PRセクション全体を生成"""
        return f"""## プルリクエストの手順

<!-- MANUAL_START:other -->
{self._generate_pr_guidelines_content(project_info)}
<!-- MANUAL_END:other -->

---
"""

    def _generate_footer(self) -> str:
        """フッター部分を生成"""
        return f"""
---

*このAGENTS.mdは自動生成されています。最終更新: {get_current_timestamp()}*
"""

    def _generate_project_overview_content(
        self, project_info: ProjectInfo, manual_sections: dict[str, str]
    ) -> str:
        """プロジェクト概要セクションの内容を生成"""
        if "description" in manual_sections:
            return manual_sections["description"]
        else:
            # デフォルトの説明を生成
            description = self._collect_project_description()
            if description:
                return f"## 概要\n\n{description}"
            else:
                return "## 概要\n\nPlease describe this project here."

    def _generate_build_commands_content(self, project_info: ProjectInfo) -> str:
        """ビルドコマンドの内容を生成"""
        build_commands = project_info.build_commands
        if build_commands:
            lines = ["```bash"]
            formatted_commands = format_commands_with_package_manager(
                build_commands, self.package_managers, "python"
            )
            lines.extend(formatted_commands)
            lines.append("```")
            return "\n".join(lines)
        else:
            return "ビルド手順は設定されていません。"

    def _generate_test_commands_content(self, project_info: ProjectInfo) -> str:
        """テストコマンドの内容を生成"""
        test_commands = project_info.test_commands
        if test_commands:
            lines = []
            llm_mode = self.agents_config.get("llm_mode", "both")

            if llm_mode in ["api", "both"]:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                formatted_commands = format_commands_with_package_manager(
                    test_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                formatted_commands = format_commands_with_package_manager(
                    test_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
            return "\n".join(lines)
        else:
            return "テストコマンドは設定されていません。"

    def _generate_custom_instructions_content(self) -> str:
        """カスタム指示の内容を生成"""
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            return "\n".join(self._generate_custom_instructions_section(custom_instructions))
        return ""

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
            self.logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _generate_project_overview(
        self, project_info: ProjectInfo, manual_sections: dict[str, str]
    ) -> list[str]:
        """プロジェクト概要セクションを生成"""
        lines = []
        lines.append("## プロジェクト概要")
        lines.append("")

        lines.append(DESCRIPTION_START)
        lines.append("")

        if "description" in manual_sections:
            lines.append(manual_sections["description"])
        else:
            # プロジェクト説明を取得
            from ..utils.markdown_utils import extract_project_description

            description = extract_project_description(self.project_root, project_info.description)
            lines.append(description)

        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else UNKNOWN}")
        lines.append("")
        lines.append(DESCRIPTION_END)
        return lines

    def _generate_setup_section(self, project_info: ProjectInfo) -> list[str]:
        """開発環境セットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")
        lines.append(SETUP_START)
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

        lines.extend(self._generate_installation_section())

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        lines.append("")
        lines.append(SETUP_END)
        return lines

    def _generate_build_test_section(self, project_info: ProjectInfo) -> list[str]:
        """ビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")
        lines.append(USAGE_START)
        lines.append("")

        # ビルド手順
        lines.append("### ビルド手順")
        lines.append("")
        build_commands = project_info.build_commands
        if build_commands:
            lines.append("```bash")
            formatted_commands = format_commands_with_package_manager(
                build_commands, self.package_managers, "python"
            )
            lines.extend(formatted_commands)
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
                formatted_commands = format_commands_with_package_manager(
                    test_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                formatted_commands = format_commands_with_package_manager(
                    test_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")
        lines.append(USAGE_END)

        return lines

    def _format_coding_standards(self, coding_standards: dict[str, Any]) -> list[str]:
        """コーディング規約のフォーマット"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")
        lines.append(OTHER_START)
        lines.append("")

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
        lines.append(OTHER_END)

        return lines

    def _generate_pr_section(self, project_info: ProjectInfo) -> list[str]:
        return super()._generate_pr_section(project_info, max_test_commands=None)

    def _convert_structured_data_to_markdown(
        self, data: AgentsDocument, project_info: ProjectInfo
    ) -> str:
        """
        構造化データをマークダウン形式に変換（テンプレート使用）

        Args:
            data: 構造化されたAGENTSドキュメントデータ
            project_info: プロジェクト情報

        Returns:
            マークダウン形式の文字列
        """
        # Extract manual sections from existing AGENTS.md
        try:
            existing_content = self.agents_path.read_text()
            manual_sections = self._extract_manual_sections(existing_content)
        except (FileNotFoundError, OSError):
            manual_sections = {}

        # 構造化データをテンプレートコンテキストに変換
        context = {
            "timestamp": get_current_timestamp(),
            "description": data.description,
            "languages": self.languages,
            "javascript": "javascript" in self.languages,
            "go": "go" in self.languages,
            "installation_steps": self._format_structured_installation(data.setup_instructions),
            "llm_setup": self._format_structured_llm_setup(data.setup_instructions),
            "build_commands": self._format_structured_build_commands(data.build_test_instructions),
            "test_commands": self._format_structured_test_commands(data.build_test_instructions),
            "coding_standards": self._format_structured_coding_standards(data.coding_standards),
            "pr_guidelines": self._format_structured_pr_guidelines(data.pr_guidelines),
            "custom_instructions": "",
        }

        # Jinja2テンプレートでレンダリング
        return self._render_template("agents_template.md.j2", context)

    def _format_structured_installation(self, setup_instructions) -> str:
        """構造化データをインストール手順にフォーマット"""
        if not setup_instructions or not setup_instructions.installation_commands:
            return "インストール手順は設定されていません。"
        return "\n".join(f"```bash\n{cmd}\n```" for cmd in setup_instructions.installation_commands)

    def _format_structured_llm_setup(self, setup_instructions) -> str:
        """構造化データをLLMセットアップにフォーマット"""
        if not setup_instructions or not setup_instructions.llm_setup:
            return "LLM環境のセットアップは設定されていません。"
        lines = []
        if setup_instructions.llm_setup.api_setup:
            lines.append("#### APIを使用する場合")
            lines.append("")
            lines.append(setup_instructions.llm_setup.api_setup)
            lines.append("")
        if setup_instructions.llm_setup.local_setup:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")
            lines.append(setup_instructions.llm_setup.local_setup)
            lines.append("")
        return "\n".join(lines).strip()

    def _format_structured_build_commands(self, build_test_instructions) -> str:
        """構造化データをビルドコマンドにフォーマット"""
        if not build_test_instructions or not build_test_instructions.build_commands:
            return "ビルド手順は設定されていません。"
        return "\n".join(f"```bash\n{cmd}\n```" for cmd in build_test_instructions.build_commands)

    def _format_structured_test_commands(self, build_test_instructions) -> str:
        """構造化データをテストコマンドにフォーマット"""
        if not build_test_instructions or not build_test_instructions.test_commands:
            return "テストコマンドは設定されていません。"
        lines = []
        llm_mode = self.agents_config.get("llm_mode", "api")
        if llm_mode in ["api", "both"]:
            lines.append("#### APIを使用する場合")
            lines.append("")
            lines.append("```bash")
            for cmd in build_test_instructions.test_commands:
                lines.append(cmd)
            lines.append("```")
            lines.append("")
        if llm_mode in ["local", "both"]:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")
            lines.append("```bash")
            for cmd in build_test_instructions.test_commands:
                lines.append(cmd)
            lines.append("```")
            lines.append("")
        return "\n".join(lines).strip()

    def _format_structured_coding_standards(self, coding_standards) -> str:
        """構造化データをコーディング規約にフォーマット"""
        if not coding_standards:
            return ""
        lines = []
        if coding_standards.formatter:
            lines.append("### フォーマッター")
            lines.append("")
            lines.append(f"- **{coding_standards.formatter}** を使用")
            if coding_standards.formatter == "black":
                lines.append("  ```bash")
                lines.append("  black .")
                lines.append("  ```")
            elif coding_standards.formatter == "prettier":
                lines.append("  ```bash")
                lines.append("  npx prettier --write .")
                lines.append("  ```")
            lines.append("")
        if coding_standards.linter:
            lines.append("### リンター")
            lines.append("")
            lines.append(f"- **{coding_standards.linter}** を使用")
            if coding_standards.linter == "ruff":
                lines.append("  ```bash")
                lines.append("  ruff check .")
                lines.append("  ruff format .")
                lines.append("  ```")
            lines.append("")
        if coding_standards.style_guide:
            lines.append("### スタイルガイド")
            lines.append("")
            lines.append(f"- {coding_standards.style_guide} に準拠")
            lines.append("")
        return "\n".join(lines).strip()

    def _format_structured_pr_guidelines(self, pr_guidelines) -> str:
        """構造化データをPRガイドラインにフォーマット"""
        if not pr_guidelines:
            return ""
        return pr_guidelines.content if pr_guidelines.content else ""
