"""
ReadmeGeneratorの追加テスト - カバレッジ向上用
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# モジュールパスを修正
sys.path.insert(0, "/home/user/projects/hamu/agents-docs-sync")

from docgen.generators.readme_generator import ReadmeGenerator, ReadmeDocument


class TestReadmeGeneratorExtended:
    """ReadmeGeneratorの拡張テスト"""

    def test_initialization_with_absolute_path(self):
        """絶対パスでの初期化テスト"""
        project_root = Path("/tmp/test_project")
        config = {"output": {"readme_doc": "/tmp/README.md"}}

        generator = ReadmeGenerator(project_root, ["python"], config)

        assert generator.output_path == Path("/tmp/README.md")

    def test_initialization_with_relative_path(self):
        """相対パスでの初期化テスト"""
        project_root = Path("/tmp/test_project")
        config = {"output": {"readme_doc": "README.md"}}

        generator = ReadmeGenerator(project_root, ["python"], config)

        assert generator.output_path == project_root / "README.md"

    def test_convert_readme_structured_data_to_markdown_empty_sections(
        self, temp_project
    ):
        """空セクションを持つ構造化データの変換テスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        data = ReadmeDocument(
            title="Test",
            description="Test desc",
            project_overview={},
            setup_instructions={},
            build_test_instructions={},
            coding_standards={},
            pr_guidelines={},
            auto_generated_note="Auto-generated",
        )

        markdown = generator._convert_readme_structured_data_to_markdown(data, {})

        assert "# Test" in markdown
        assert "Test desc" in markdown
        assert "Auto-generated" in markdown

    def test_generate_template_with_minimal_info(self, temp_project):
        """最小情報でのテンプレート生成テスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        project_info = {"description": "Minimal project"}

        result = generator._generate_template(project_info)

        assert "# README" in result
        assert "Minimal project" in result

    def test_generate_template_with_full_info(self, temp_project):
        """完全情報でのテンプレート生成テスト"""
        generator = ReadmeGenerator(temp_project, ["python", "javascript"], {})

        project_info = {
            "description": "Full project",
            "dependencies": {
                "python": ["pytest", "black"],
                "javascript": ["jest", "webpack"],
            },
            "build_commands": ["npm run build", "python setup.py build"],
            "test_commands": ["pytest", "npm test"],
            "lint_commands": ["flake8", "eslint"],
            "dev_commands": ["npm run dev", "python -m http.server"],
        }

        result = generator._generate_template(project_info)

        assert "# README" in result
        assert "Full project" in result
        assert "pytest" in result
        assert "jest" in result
        assert "npm run build" in result

    def test_dependency_detection_python(self, temp_project):
        """Python依存関係検出テスト"""
        # requirements.txtを作成
        (temp_project / "requirements.txt").write_text("pytest>=7.0.0\nblack\n")
        (temp_project / "pyproject.toml").write_text(
            '[project]\ndependencies = ["requests"]\n'
        )

        generator = ReadmeGenerator(temp_project, ["python"], {})

        dependencies = generator._detect_dependencies()

        assert "python" in dependencies
        assert "pytest" in dependencies["python"]
        assert "black" in dependencies["python"]
        assert "requests" in dependencies["python"]

    def test_dependency_detection_javascript(self, temp_project):
        """JavaScript依存関係検出テスト"""
        (temp_project / "package.json").write_text(
            '{"dependencies": {"react": "^18.0.0", "lodash": "^4.17.21"}}'
        )

        generator = ReadmeGenerator(temp_project, ["javascript"], {})

        dependencies = generator._detect_dependencies()

        assert "javascript" in dependencies
        assert "react" in dependencies["javascript"]
        assert "lodash" in dependencies["javascript"]

    def test_dependency_detection_go(self, temp_project):
        """Go依存関係検出テスト"""
        (temp_project / "go.mod").write_text(
            "module example\n\ngo 1.19\nrequire github.com/gin-gonic/gin v1.9.0\n"
        )

        generator = ReadmeGenerator(temp_project, ["go"], {})

        dependencies = generator._detect_dependencies()

        assert "go" in dependencies
        assert "gin-gonic/gin" in dependencies["go"]

    def test_manual_sections_extraction(self, temp_project):
        """手動セクション抽出テスト"""
        readme_content = """# README

<!-- MANUAL_START:description -->
This is manual description
<!-- MANUAL_END:description -->

## Installation

```bash
pip install -r requirements.txt
```

<!-- MANUAL_START:installation -->
npm install
<!-- MANUAL_END:installation -->
"""

        (temp_project / "README.md").write_text(readme_content)

        generator = ReadmeGenerator(temp_project, ["python"], {})

        manual_sections = generator._extract_manual_sections()

        assert "description" in manual_sections
        assert manual_sections["description"] == "This is manual description"
        assert "installation" in manual_sections
        assert manual_sections["installation"] == "npm install"

    def test_manual_sections_preservation(self, temp_project):
        """手動セクション保持テスト"""
        manual_sections = {
            "description": "Manual description",
            "installation": "Manual installation",
            "usage": "Manual usage",
        }

        generator = ReadmeGenerator(temp_project, ["python"], {})

        preserved = generator._preserve_manual_sections(manual_sections)

        assert "Manual description" in preserved
        assert "Manual installation" in preserved
        assert "Manual usage" in preserved
        assert "<!-- MANUAL_START:" in preserved
        assert "<!-- MANUAL_END:" in preserved

    def test_format_project_info_for_readme_prompt(self, temp_project):
        """READMEプロンプト用プロジェクト情報フォーマットテスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        project_info = {
            "description": "Test project",
            "dependencies": {"python": ["pytest", "black"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest"],
            "lint_commands": ["flake8"],
            "dev_commands": ["python -m http.server"],
        }

        formatted = generator._format_project_info_for_readme_prompt(project_info)

        assert "Test project" in formatted
        assert "pytest" in formatted
        assert "black" in formatted
        assert "python setup.py build" in formatted
        assert "flake8" in formatted

    def test_format_manual_sections_for_prompt(self, temp_project):
        """手動セクションのプロンプトフォーマットテスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        manual_sections = {
            "description": "Manual description",
            "installation": "Manual installation steps",
        }

        formatted = generator._format_manual_sections_for_prompt(manual_sections)

        assert "Manual description" in formatted
        assert "Manual installation steps" in formatted

    def test_generate_with_no_languages(self, temp_project):
        """言語なしでの生成テスト"""
        generator = ReadmeGenerator(temp_project, [], {})

        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

    def test_generate_with_multiple_languages(self, temp_project):
        """複数言語での生成テスト"""
        # Pythonファイル
        (temp_project / "main.py").write_text("print('hello')")
        # JavaScriptファイル
        (temp_project / "app.js").write_text("console.log('hello')")

        generator = ReadmeGenerator(temp_project, ["python", "javascript"], {})

        result = generator.generate()

        assert result is True
        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "python" in content.lower() or "javascript" in content.lower()

    def test_readme_document_model_validation(self):
        """ReadmeDocumentモデル検証テスト"""
        # 最小データでの作成
        doc = ReadmeDocument(
            title="Test README",
            description="Test desc",
            project_overview={},
            setup_instructions={},
            build_test_instructions={},
            coding_standards={},
            pr_guidelines={},
            auto_generated_note="",
        )

        assert doc.title == "Test README"
        assert doc.description == "Test desc"
        assert doc.auto_generated_note == ""

    def test_error_handling_in_generation(self, temp_project):
        """生成時のエラーハンドリングテスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        # プロジェクト情報収集でエラーを発生させる
        with patch.object(
            generator.collector, "collect", side_effect=Exception("Collection error")
        ):
            result = generator.generate()

            assert result is False

    def test_missing_output_directory(self, temp_project):
        """出力ディレクトリがない場合のテスト"""
        output_dir = temp_project / "output"
        config = {"output": {"readme_doc": str(output_dir / "README.md")}}

        generator = ReadmeGenerator(temp_project, ["python"], config)

        result = generator.generate()

        assert result is True
        assert output_dir.exists()
        assert (output_dir / "README.md").exists()

    def test_empty_manual_sections_handling(self, temp_project):
        """空の手動セクション処理テスト"""
        readme_content = """# README

<!-- MANUAL_START:description -->
<!-- MANUAL_END:description -->

<!-- MANUAL_START:installation -->
<!-- MANUAL_END:installation -->
"""

        (temp_project / "README.md").write_text(readme_content)

        generator = ReadmeGenerator(temp_project, ["python"], {})

        manual_sections = generator._extract_manual_sections()

        assert "description" in manual_sections
        assert manual_sections["description"] == ""
        assert "installation" in manual_sections
        assert manual_sections["installation"] == ""

    def test_malformed_manual_sections_handling(self, temp_project):
        """不正な形式の手動セクション処理テスト"""
        readme_content = """# README

<!-- MANUAL_START:description -->
This is manual description
<!-- MANUAL_END:installation -->

Missing end tag for description
"""

        (temp_project / "README.md").write_text(readme_content)

        generator = ReadmeGenerator(temp_project, ["python"], {})

        # 不正な形式でもエラーにならないことを確認
        manual_sections = generator._extract_manual_sections()

        assert isinstance(manual_sections, dict)

    def test_dependency_detection_no_files(self, temp_project):
        """依存関係ファイルがない場合のテスト"""
        generator = ReadmeGenerator(temp_project, ["python"], {})

        dependencies = generator._detect_dependencies()

        assert dependencies == {}

    def test_dependency_detection_empty_files(self, temp_project):
        """空の依存関係ファイルの場合のテスト"""
        (temp_project / "requirements.txt").write_text("")
        (temp_project / "package.json").write_text("{}")
        (temp_project / "go.mod").write_text("")

        generator = ReadmeGenerator(temp_project, ["python", "javascript", "go"], {})

        dependencies = generator._detect_dependencies()

        assert "python" in dependencies
        assert "javascript" in dependencies
        assert "go" in dependencies
        # 空なので依存関係はない
        assert dependencies["python"] == []
        assert dependencies["javascript"] == []
        assert dependencies["go"] == []
