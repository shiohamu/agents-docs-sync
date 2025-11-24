"""
README generation module
Achieve structured output with Outlines integration
"""

from pathlib import Path
import re
from typing import Any

from ..models import ProjectInfo, ReadmeDocument
from ..utils.markdown_utils import (
    DESCRIPTION_END,
    DESCRIPTION_START,
    OTHER_END,
    OTHER_START,
    SECTION_SEPARATOR,
    SETUP_END,
    SETUP_START,
    USAGE_END,
    USAGE_START,
)
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

    @property
    def readme_path(self):
        return self.output_path

    def _get_mode_key(self) -> str:
        return "readme_mode"

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
2. セットアップ手順
3. 使用方法
4. 技術スタック
5. その他の情報

重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

        return prompt

    def _get_project_overview_section(self, content: str) -> str:
        return self._extract_description_section(content)

    def _generate_project_overview(self, project_info: ProjectInfo) -> list[str]:
        """README用のプロジェクト概要セクションを生成"""
        lines = []
        lines.append("## 概要")
        lines.append("")

        # プロジェクト説明を取得
        from ..utils.markdown_utils import extract_project_description

        description = extract_project_description(
            self.project_root, project_info.description, self.readme_path
        )
        lines.append(description)

        return lines

    def _generate_build_test_section(self, project_info: ProjectInfo) -> list[str]:
        """README用のビルド/テストセクションを生成"""
        lines = []
        build_commands = project_info.build_commands
        test_commands = project_info.test_commands
        if build_commands or test_commands:
            lines.append("## ビルドおよびテスト")
            lines.append("")

            if build_commands:
                lines.append("### ビルド")
                lines.append("")
                lines.append("```bash")
                from ..utils.markdown_utils import format_commands_with_package_manager

                formatted_commands = format_commands_with_package_manager(
                    build_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")

            if test_commands:
                lines.append("### テスト")
                lines.append("")
                lines.append("```bash")
                formatted_commands = format_commands_with_package_manager(
                    test_commands, self.package_managers, "python"
                )
                lines.extend(formatted_commands)
                lines.append("```")
                lines.append("")

        return lines

    def _generate_coding_standards_section(self, project_info: ProjectInfo) -> list[str]:
        """README用のコーディング規約セクションを生成"""
        lines = []
        coding_standards = project_info.coding_standards or {}

        if coding_standards:
            lines.append("## コーディング規約")
            lines.append("")

            # フォーマッター
            formatter = coding_standards.get("formatter")
            if formatter:
                lines.append(f"- **フォーマッター**: {formatter}")

            # リンター
            linter = coding_standards.get("linter")
            if linter:
                lines.append(f"- **リンター**: {linter}")

            # スタイルガイド
            style_guide = coding_standards.get("style_guide")
            if style_guide:
                lines.append(f"- **スタイルガイド**: {style_guide}")

            lines.append("")
        else:
            lines.append("## コーディング規約")
            lines.append("")
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_pr_section(self, project_info: ProjectInfo) -> list[str]:
        """README用のPRセクションを生成"""
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
        for cmd in test_commands[:3]:
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
        """README用のカスタム指示セクションを生成"""
        lines = []
        if custom_instructions:
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

        return lines

    def _convert_structured_data_to_markdown(self, data, project_info: ProjectInfo) -> str:
        """READMEの構造化データをマークダウン形式に変換"""
        lines = []

        # タイトル
        lines.append(f"# {data.title}")
        lines.append("")

        # Description (prioritize manual sections)
        description = getattr(data, "description", "")
        if description:
            lines.append(description)
        lines.append("")

        # Technologies used
        if hasattr(data, "technologies") and data.technologies:
            lines.append("## Technologies Used")
            lines.append("")
            for tech in data.technologies:
                lines.append(f"- {tech}")
            lines.append("")

        # 依存関係
        if hasattr(data, "dependencies") and data.dependencies:
            lines.append("## 依存関係")
            lines.append("")
            for lang, deps in data.dependencies.items():
                if deps:
                    lines.append(f"### {lang}")
                    lines.append("")
                    for dep in deps:
                        lines.append(f"- {dep}")
                    lines.append("")

        # セットアップ
        if hasattr(data, "setup_instructions") and data.setup_instructions:
            lines.append("## セットアップ")
            lines.append("")

            prerequisites = data.setup_instructions.get("prerequisites", [])
            if prerequisites:
                lines.append("### Prerequisites")
                lines.append("")
                for prereq in prerequisites:
                    lines.append(f"- {prereq}")
                lines.append("")

            installation_steps = data.setup_instructions.get("installation_steps", [])
            if installation_steps:
                lines.append("### インストール")
                lines.append("")
                lines.append("```bash")
                for step in installation_steps:
                    lines.append(step)
                lines.append("```")
                lines.append("")

        # Project structure
        if hasattr(data, "project_structure") and data.project_structure:
            lines.append("## Project Structure")
            lines.append("")
            for item in data.project_structure:
                lines.append(f"- {item}")
            lines.append("")

        # ビルドおよびテスト
        if (hasattr(data, "build_commands") and data.build_commands) or (
            hasattr(data, "test_commands") and data.test_commands
        ):
            lines.append("## ビルドおよびテスト")
            lines.append("")

            if hasattr(data, "build_commands") and data.build_commands:
                lines.append("### ビルド")
                lines.append("")
                lines.append("```bash")
                for cmd in data.build_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")

            if hasattr(data, "test_commands") and data.test_commands:
                lines.append("### テスト")
                lines.append("")
                lines.append("```bash")
                for cmd in data.test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")

        return "\n".join(lines)

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
        Generate README based on template (existing implementation)

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

        lines = []

        # Project name (inferred from directory name)
        project_name = self.project_root.name
        lines.append(f"# {project_name}")
        lines.append("")

        # Manual section: Description
        lines.append(DESCRIPTION_START)
        if "description" in manual_sections:
            lines.append(manual_sections["description"])
        else:
            # Collect project description
            description = self._collect_project_description()
            if description:
                lines.append("## 概要")
                lines.append("")
                lines.append(description)
            else:
                lines.append("## 概要")
                lines.append("")
                lines.append("Please describe this project here.")
        lines.append(DESCRIPTION_END)
        lines.append("")

        # Auto-generated section: Technologies used
        lines.append("## Technologies Used")
        lines.append("")
        if self.languages:
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
            for lang in self.languages:
                display_name = lang_display.get(lang, lang.capitalize())
                lines.append(f"- {display_name}")
        else:
            lines.append("- Not detected")
        lines.append("")

        # Dependency information
        dependencies = self._detect_dependencies()
        if dependencies:
            lines.append("## 依存関係")
            lines.append("")
            for dep_type, deps in dependencies.items():
                if deps:
                    lines.append(f"### {dep_type}")
                    lines.append("")
                    for dep in deps[:10]:  # Show up to 10
                        lines.append(f"- {dep}")
                    if len(deps) > 10:
                        lines.append(f"- ... 他 {len(deps) - 10} 個")
                    lines.append("")

        # セットアップ手順
        lines.append("## セットアップ")
        lines.append("")
        lines.append(SETUP_START)
        if "setup" in manual_sections:
            # 手動セクションがある場合は、パッケージマネージャに基づいて内容を更新
            updated_setup = self._update_manual_setup_section(manual_sections["setup"])
            lines.append(updated_setup)
        else:
            # 自動生成
            lines.extend(self._generate_setup_section())
        lines.append(SETUP_END)
        lines.append("")

        # 使用方法
        if "usage" in manual_sections:
            lines.append("## 使用方法")
            lines.append("")
            lines.append(USAGE_START)
            lines.append(manual_sections["usage"])
            lines.append(USAGE_END)
            lines.append("")

        # ビルドおよびテスト
        project_info = self.collector.collect_all()
        build_commands = project_info.build_commands
        test_commands = project_info.test_commands
        if build_commands or test_commands:
            lines.append("## ビルドおよびテスト")
            lines.append("")

            if build_commands:
                lines.append("### ビルド")
                lines.append("")
                lines.append("```bash")
                for cmd in build_commands[:5]:  # 最大5個まで表示
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    display_cmd = cmd
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if cmd.startswith("python") and not cmd.startswith("uv run"):
                            display_cmd = f"uv run {cmd}"
                    lines.append(display_cmd)
                if len(build_commands) > 5:
                    lines.append("# ... その他のビルドコマンド")
            lines.append("```")
            lines.append("")

        test_commands = project_info.test_commands
        if test_commands:
            lines.append("### テスト")
            lines.append("")
            lines.append("```bash")
            for cmd in test_commands[:5]:  # 最大5個まで表示
                # uvプロジェクトの場合はpythonコマンドにuv runをつける
                display_cmd = cmd
                if "python" in self.package_managers and self.package_managers["python"] == "uv":
                    if (
                        cmd.startswith("python") or cmd.startswith("pytest")
                    ) and not cmd.startswith("uv run"):
                        display_cmd = f"uv run {cmd}"
                lines.append(display_cmd)
            if len(test_commands) > 5:
                lines.append("# ... その他のテストコマンド")
            lines.append("```")
            lines.append("")

        # 手動セクション: その他
        if "other" in manual_sections:
            lines.append(OTHER_START)
            lines.append(manual_sections["other"])
            lines.append(OTHER_END)
            lines.append("")

        # フッター
        lines.append(SECTION_SEPARATOR)
        lines.append("")
        lines.append(self._generate_footer())
        lines.append("")

        return "\n".join(lines)

    def _update_manual_setup_section(self, manual_content: str) -> str:
        """
        手動セットアップセクションをパッケージマネージャに基づいて更新

        Args:
            manual_content: 手動セクションの内容

        Returns:
            更新された内容
        """
        pm_python = self.package_managers.get("python", "pip")
        pm_js = self.package_managers.get("javascript", "npm")

        # Pythonのインストールコマンドを置き換え
        if pm_python == "uv":
            # uv syncに置き換え
            manual_content = manual_content.replace(
                "pip install -r requirements-docgen.txt\npip install -r requirements-test.txt",
                "uv sync",
            )
            # 個別の行も置き換え
            manual_content = manual_content.replace(
                "pip install -r requirements-docgen.txt", "uv sync"
            )
            manual_content = manual_content.replace("pip install -r requirements-test.txt", "")
            # 個別のpip installも置き換え
            manual_content = re.sub(
                r"pip install -r requirements-docgen\.txt", "uv sync", manual_content
            )
            manual_content = re.sub(r"pip install -r requirements-test\.txt", "", manual_content)
        elif pm_python == "poetry":
            manual_content = re.sub(
                r"pip install -r requirements-docgen\.txt\npip install -r requirements-test\.txt",
                "poetry install",
                manual_content,
            )
            manual_content = re.sub(
                r"pip install -r requirements-docgen\.txt", "poetry install", manual_content
            )
            manual_content = re.sub(r"pip install -r requirements-test\.txt", "", manual_content)

        # JavaScriptのインストールコマンドを置き換え
        if pm_js == "pnpm":
            manual_content = manual_content.replace("npm install", "pnpm install")
        elif pm_js == "yarn":
            manual_content = manual_content.replace("npm install", "yarn install")

        # 重複する空行を削除
        manual_content = re.sub(r"\n\n\n+", "\n\n", manual_content)

        return manual_content

    def _generate_setup_section(self) -> list[str]:
        """
        Detect dependencies

        Returns:
            Dictionary with dependency types as keys and dependency lists as values
        """
        lines = []

        lines.append("### 必要な環境")
        lines.append("")
        if "python" in self.languages:
            lines.append("- Python 3.8以上")
        if "javascript" in self.languages or "typescript" in self.languages:
            lines.append("- Node.js (推奨バージョン: 18以上)")
        if "go" in self.languages:
            lines.append("- Go 1.16以上")
        lines.append("")
        lines.append("### インストール")
        lines.append("")

        if "python" in self.languages:
            pm = self.package_managers.get("python", "pip")
            lines.append("```bash")
            if pm == "uv":
                lines.append("uv sync")
            elif pm == "poetry":
                lines.append("poetry install")
            elif pm == "conda":
                lines.append("conda env create -f environment.yml")
            else:  # pip
                lines.append("pip install -r requirements.txt")
            lines.append("```")
            lines.append("")

        if "javascript" in self.languages or "typescript" in self.languages:
            pm = self.package_managers.get("javascript", "npm")
            lines.append("```bash")
            if pm == "pnpm":
                lines.append("pnpm install")
            elif pm == "yarn":
                lines.append("yarn install")
            else:  # npm
                lines.append("npm install")
            lines.append("```")
            lines.append("")

        if "go" in self.languages:
            pm = self.package_managers.get("go", "go")
            lines.append("```bash")
            if pm == "dep":
                lines.append("dep ensure")
            elif pm == "glide":
                lines.append("glide install")
            else:  # go modules
                lines.append("go mod download")
            lines.append("```")
            lines.append("")

        return lines

    def _detect_dependencies(self) -> dict[str, list[str]]:
        """
        Detect dependencies
        """
        dependencies = {}

        # Python依存関係
        if "python" in self.languages:
            req_file = self.project_root / "requirements.txt"
            if req_file.exists():
                import re

                deps = []
                # PEP 440バージョン指定子のパターン（==, >=, <=, !=, ~=, >, <, ===）
                version_spec_pattern = re.compile(r"[=!<>~]+")

                for line in req_file.read_text(encoding="utf-8").split("\n"):
                    line = line.strip()
                    # コメント行や空行をスキップ
                    if not line or line.startswith("#"):
                        continue

                    # URLやファイルパスの場合はスキップ（-e, @などで始まる行）
                    if line.startswith("-e ") or line.startswith("@") or "://" in line:
                        continue

                    # バージョン指定子の前までをパッケージ名として抽出
                    # 例: "requests!=2.28.0" -> "requests"
                    # 例: "django~=4.0" -> "django"
                    match = version_spec_pattern.search(line)
                    if match:
                        package_name = line[: match.start()].strip()
                    else:
                        # バージョン指定子がない場合（パッケージ名のみ）
                        package_name = line.split()[0] if line.split() else line

                    # パッケージ名が有効な場合のみ追加
                    if package_name:
                        deps.append(package_name)

                if deps:
                    dependencies["Python"] = deps

        # JavaScript依存関係
        if "javascript" in self.languages or "typescript" in self.languages:
            package_file = self.project_root / "package.json"
            if package_file.exists():
                import json

                try:
                    with open(package_file, encoding="utf-8") as f:
                        package_data = json.load(f)
                        deps = []
                        if "dependencies" in package_data:
                            deps.extend(list(package_data["dependencies"].keys()))
                        if "devDependencies" in package_data:
                            deps.extend(list(package_data["devDependencies"].keys()))
                        if deps:
                            dependencies["Node.js"] = deps
                except:
                    pass

        # Go依存関係
        if "go" in self.languages:
            go_mod = self.project_root / "go.mod"
            if go_mod.exists():
                deps = []
                lines = go_mod.read_text(encoding="utf-8").split("\n")
                in_require_block = False

                for line in lines:
                    line = line.strip()

                    # 複数行のrequireブロックの開始を検出
                    if line.startswith("require ("):
                        in_require_block = True
                        continue

                    # 複数行のrequireブロックの終了を検出
                    if in_require_block and line == ")":
                        in_require_block = False
                        continue

                    # ブロック内の依存関係を抽出
                    if in_require_block:
                        # 空行やコメントをスキップ
                        if not line or line.startswith("//"):
                            continue
                        parts = line.split()
                        if len(parts) >= 1:
                            deps.append(parts[0])

                    # 単一行のrequireを検出
                    elif line.startswith("require ") and not line.startswith("require ("):
                        parts = line.split()
                        if len(parts) >= 2:
                            deps.append(parts[1])

                if deps:
                    dependencies["Go"] = deps

        return dependencies
