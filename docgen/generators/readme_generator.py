"""
README generation module
Achieve structured output with Outlines integration
"""

from pathlib import Path
from typing import Any

from ..models.project import ProjectInfo
from ..models.readme import ReadmeDocument
from .base_generator import BaseGenerator


class ReadmeGenerator(BaseGenerator):
    """README generation class"""

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
    ):
        """
        Initialize

        Args:
            project_root: Project root directory
            languages: List of detected languages
            config: Configuration dictionary
            package_managers: Dictionary of detected package managers
        """
        super().__init__(project_root, languages, config, package_managers)
        self.preserve_manual = config.get("generation", {}).get("preserve_manual_sections", True)

    def _should_use_llm(self) -> bool:
        """README generation uses LLM based on mode setting"""
        generation_config = self.agents_config.get("generation", {})
        mode = generation_config.get(self._get_mode_key(), "template")
        return mode in ["llm", "hybrid"]

    @property
    def readme_path(self):
        return self.output_path

    def _get_mode_key(self) -> str:
        return "readme_mode"

    def _generate_markdown(self, project_info: ProjectInfo) -> str:
        """
        README用のマークダウンを生成（モード設定を正しく取得）
        """
        # generation設定を取得（agents_configから）
        generation_config = self.agents_config.get("generation", {})
        mode = generation_config.get(self._get_mode_key(), "template")

        if mode == "llm":
            # LLM完全生成
            return self._generate_with_llm(project_info)
        elif mode == "hybrid":
            # ハイブリッド生成
            return self._generate_hybrid(project_info)
        else:
            # テンプレート生成（デフォルト）
            return self._generate_template(project_info)

    def _get_output_key(self) -> str:
        return "readme"

    def _get_document_type(self) -> str:
        return "README.md"

    def _get_structured_model(self):
        return ReadmeDocument

    def _create_llm_prompt(self, project_info: ProjectInfo) -> str:
        return self._create_readme_prompt(project_info)

    def _create_readme_prompt(self, project_info: ProjectInfo) -> str:
        """README生成用のLLMプロンプトを作成"""
        prompt = f"""以下のプロジェクト情報を基に、README.mdドキュメントを生成してください。

{self._format_project_info_for_prompt(project_info)}

以下のセクションを含めてください:
1. プロジェクト名と概要
2. セットアップ手順、インストール方法
3. 使用方法、使用例
4. コマンドの例
5. 技術スタック
6. その他の情報

重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

        return prompt

    def _convert_structured_data_to_markdown(self, data, project_info: ProjectInfo) -> str:
        """READMEの構造化データをマークダウン形式に変換（未使用）"""
        # LLM生成では直接マークダウンを生成するため、このメソッドは使用しない
        return ""

    def _get_project_overview_section(self, content: str) -> str:
        """プロジェクト概要セクションを取得"""
        return self._extract_description_section(content)

    def _collect_project_description(self) -> str:
        """プロジェクト説明を収集"""
        from ..utils.markdown_utils import extract_project_description

        return extract_project_description(self.project_root, "", self.readme_path)

    def _generate_setup_from_project_info(self, project_info: ProjectInfo) -> str:
        """プロジェクト情報からセットアップセクションを生成"""
        # セットアップ用のコンテキストを作成
        # package_managersが空の場合は自動検出
        if not self.package_managers:
            from ..language_detector import LanguageDetector

            detector = LanguageDetector(self.project_root)
            detector.detect_languages()
            self.package_managers = detector.get_detected_package_managers()

        setup_context = {
            "has_python": "python" in self.languages,
            "has_javascript": "javascript" in self.languages or "typescript" in self.languages,
            "has_go": "go" in self.languages,
            "python_pm": self.package_managers.get("python", "pip"),
            "js_pm": self.package_managers.get("javascript", "npm"),
        }

        # セットアップ用のサブテンプレートをレンダリング
        return self._render_template("setup_template.md.j2", setup_context)

    def _format_languages(self) -> str:
        """言語リストをフォーマット"""
        lang_display = {
            "python": "Python",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "go": "Go",
            "rust": "Rust",
            "java": "Java",
            "cpp": "C++",
            "c": "C",
            "ruby": "Ruby",
            "php": "PHP",
        }
        parts = []
        for lang in self.languages:
            display_name = lang_display.get(lang, lang.capitalize())
            parts.append(f"- {display_name}")
        return "\n".join(parts) if parts else "- Not detected"

    def _format_dependencies(self) -> str:
        """依存関係をフォーマット"""
        # 簡易的な依存関係検出
        dependencies = {}
        if "python" in self.languages:
            # pyproject.tomlから依存関係を読み取る
            pyproject_file = self.project_root / "pyproject.toml"
            if pyproject_file.exists():
                try:
                    import tomllib

                    with open(pyproject_file, "rb") as f:
                        data = tomllib.load(f)
                        deps = []
                        if "project" in data and "dependencies" in data["project"]:
                            deps = data["project"]["dependencies"]
                        elif (
                            "tool" in data
                            and "poetry" in data["tool"]
                            and "dependencies" in data["tool"]["poetry"]
                        ):
                            deps = list(data["tool"]["poetry"]["dependencies"].keys())
                        if deps:
                            dependencies["Python"] = deps[:10]  # 最大10個
                except:
                    pass

            # requirements.txtも確認
            req_file = self.project_root / "requirements.txt"
            if req_file.exists() and "Python" not in dependencies:
                deps = []
                content_lines = req_file.read_text(encoding="utf-8").split("\n")
                for line in content_lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        package_name = line.split()[0] if line.split() else line
                        if package_name:
                            deps.append(package_name)
                if deps:
                    dependencies["Python"] = deps[:10]  # 最大10個

        if "javascript" in self.languages or "typescript" in self.languages:
            package_file = self.project_root / "package.json"
            if package_file.exists():
                import json

                try:
                    with open(package_file, encoding="utf-8") as f:
                        package_data = json.load(f)
                        deps = []
                        if "dependencies" in package_data:
                            deps.extend(list(package_data["dependencies"].keys())[:10])
                        if deps:
                            dependencies["Node.js"] = deps
                except:
                    pass

        if dependencies:
            parts = []
            for dep_type, deps in dependencies.items():
                parts.append(f"### {dep_type}\n")
                for dep in deps:
                    parts.append(f"- {dep}\n")
                parts.append("\n")
            return "".join(parts).rstrip()
        return ""

    def _format_commands(self, commands) -> str:
        """コマンドリストをフォーマット"""
        if not commands:
            return ""
        parts = ["```bash"]
        for cmd in commands[:5]:  # 最大5個
            parts.append(cmd)
        if len(commands) > 5:
            parts.append("# ... その他のコマンド")
        parts.append("```")
        return "\n".join(parts)

    def _format_manual_sections_for_prompt(self, manual_sections: dict[str, str]) -> str:
        """
        Format manual sections for prompt

        Args:
            manual_sections: Manual sections

        Returns:
            Formatted string
        """
        if not manual_sections:
            return "なし"

        lines = []
        for name, content in manual_sections.items():
            lines.append(f"{name}: {content[:200]}...")  # First 200 characters

        return "\n".join(lines)

    def _generate_template(self, project_info: ProjectInfo) -> str:
        """
        Jinja2テンプレートを使用してREADMEを生成

        Args:
            project_info: Project info

        Returns:
            README content
        """
        # Extract manual sections from existing README
        try:
            existing_content = self.readme_path.read_text()
            manual_sections = self._extract_manual_sections(existing_content)
        except (FileNotFoundError, OSError):
            manual_sections = {}

        # コンテキストの準備
        context = {
            "project_name": self.project_root.name or "agents-docs-sync",
            "description_section": manual_sections.get("description", "").strip()
            or project_info.description
            or self._collect_project_description(),
            "technologies": self._format_languages(),
            "dependencies_section": self._format_dependencies(),
            "setup_section": manual_sections.get("setup", "").strip()
            or self._generate_setup_from_project_info(project_info),
            "usage_section": manual_sections.get("usage", ""),
            "build_commands": self._format_commands(project_info.build_commands),
            "test_commands": self._format_commands(project_info.test_commands),
            "other_section": manual_sections.get("other", ""),
            "footer": self._generate_footer(),
        }

        # Jinja2テンプレートでレンダリング
        return self._render_template("readme_template.md.j2", context)

    def _create_overview_prompt(self, project_info: ProjectInfo, existing_overview: str) -> str:
        """README生成用のLLMプロンプトを作成（BaseGeneratorのオーバーライド）"""
        return f"""以下のプロジェクト情報を基に、README.mdの「プロジェクト概要」セクションの内容を改善してください。
既存のテンプレート生成内容を参考に、より詳細で有用な説明を生成してください。

プロジェクト情報:
{self._format_project_info_for_prompt(project_info)}

既存のテンプレート生成内容:
{existing_overview}

改善されたプロジェクト概要の内容をマークダウン形式で出力してください。
ヘッダー（## プロジェクト概要）は含めないでください。内容のみを出力してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
手動セクションのマーカー（<!-- MANUAL_START:... --> など）は含めないでください。内容のみを出力してください。"""

    def _replace_overview_section(self, content: str, new_overview: str) -> str:
        """
        プロジェクト概要セクションを置き換え（BaseGeneratorのオーバーライド）
        READMEではdescriptionセクションを置き換える
        """
        import re

        # description_sectionの内容を置き換え
        # パターン: MANUAL_START:description ... MANUAL_END:description の後から、次のセクション（## 使用技術など）の前まで
        pattern = r"(<!-- MANUAL_START:description -->\n<!-- MANUAL_END:description -->\n)(.*?)(\n## 使用技術)"
        replacement = r"\1" + new_overview + r"\3"

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        return updated_content

    def _generate_description_section(self, manual_sections: dict[str, str]) -> str:
        """説明セクションの内容を生成"""
        if "description" in manual_sections:
            return manual_sections["description"]
        else:
            description = self._collect_project_description()
            if description:
                return description
            else:
                return "Please describe this project here."
