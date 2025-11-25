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
            "llm_mode": self.agents_config.get("llm_mode", "both"),
            "package_managers": self.package_managers,
            "build_commands": project_info.build_commands or [],
            "test_commands": project_info.test_commands or [],
            "coding_standards": project_info.coding_standards or {},
            "custom_instructions": self._generate_custom_instructions_content(),
        }

        # Jinja2テンプレートでレンダリング
        return self._render_template("agents_template.md.j2", context)

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

    def _generate_custom_instructions_content(self) -> str:
        """カスタム指示の内容を生成"""
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            return "\n".join(self._generate_custom_instructions_section(custom_instructions))
        return ""

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
        # LLM生成の場合は手動セクションを抽出しない（LLM出力を優先）
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

        # 構造化データをマークダウンに変換（未使用）
        return ""
