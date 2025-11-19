"""
AgentsGeneratorの追加テスト - カバレッジ向上用（修正版）
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# モジュールパスを修正
sys.path.insert(0, "/home/user/projects/hamu/agents-docs-sync")

from docgen.generators.agents_generator import AgentsGenerator, AgentsDocument


class TestAgentsGeneratorExtended:
    """AgentsGeneratorの拡張テスト"""

    def test_initialization_with_absolute_path(self):
        """絶対パスでの初期化テスト"""
        project_root = Path("/tmp/test_project")
        config = {"output": {"agents_doc": "/tmp/AGENTS.md"}}

        generator = AgentsGenerator(project_root, ["python"], config)

        assert generator.output_path == Path("/tmp/AGENTS.md")

    def test_initialization_with_relative_path(self):
        """相対パスでの初期化テスト"""
        project_root = Path("/tmp/test_project")
        config = {"output": {"agents_doc": "AGENTS.md"}}

        generator = AgentsGenerator(project_root, ["python"], config)

        assert generator.output_path == project_root / "AGENTS.md"

    def test_convert_structured_data_to_markdown_empty_sections(self, temp_project):
        """空セクションを持つ構造化データの変換テスト"""
        generator = AgentsGenerator(temp_project, ["python"], {})

        data = AgentsDocument(
            title="Test",
            description="Test desc",
            project_overview={},
            setup_instructions={},
            build_test_instructions={},
            coding_standards={},
            pr_guidelines={},
            auto_generated_note="Auto-generated",
        )

        markdown = generator._convert_structured_data_to_markdown(data, {})

        assert "# Test" in markdown
        assert "Test desc" in markdown
        assert "Auto-generated" in markdown

    def test_generate_template_with_minimal_info(self, temp_project):
        """最小情報でのテンプレート生成テスト"""
        generator = AgentsGenerator(temp_project, ["python"], {})

        project_info = {"description": "Minimal project"}

        result = generator._generate_template(project_info)

        assert "# AGENTS ドキュメント" in result
        assert "Minimal project" in result

    def test_generate_template_with_full_info(self, temp_project):
        """完全情報でのテンプレート生成テスト"""
        generator = AgentsGenerator(temp_project, ["python", "javascript"], {})

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

        assert "# AGENTS ドキュメント" in result
        assert "Full project" in result
        assert "pytest" in result
        assert "npm run build" in result

    def test_generate_hybrid_template_fallback(self, temp_project):
        """ハイブリッド生成のテンプレートフォールバックテスト"""
        generator = AgentsGenerator(
            temp_project, ["python"], {"agents": {"llm_mode": "both"}}
        )

        project_info = {"description": "Test project"}

        with patch.object(generator, "_generate_with_llm", return_value=None):
            result = generator._generate_hybrid(project_info)

            assert result is not None
            assert "Test project" in result

    def test_generate_hybrid_both_fail(self, temp_project):
        """ハイブリッド生成の両方失敗テスト"""
        generator = AgentsGenerator(
            temp_project, ["python"], {"agents": {"llm_mode": "both"}}
        )

        project_info = {"description": "Test project"}

        with patch.object(generator, "_generate_template", return_value=None):
            with patch.object(generator, "_generate_with_llm", return_value=None):
                result = generator._generate_hybrid(project_info)

                assert result is None

    def test_generate_with_no_languages(self, temp_project):
        """言語なしでの生成テスト"""
        generator = AgentsGenerator(temp_project, [], {})

        result = generator.generate()

        assert result is True
        assert (temp_project / "AGENTS.md").exists()

    def test_generate_with_multiple_languages(self, temp_project):
        """複数言語での生成テスト"""
        # Pythonファイル
        (temp_project / "main.py").write_text("print('hello')")
        # JavaScriptファイル
        (temp_project / "app.js").write_text("console.log('hello')")

        generator = AgentsGenerator(temp_project, ["python", "javascript"], {})

        result = generator.generate()

        assert result is True
        content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
        assert "python" in content.lower() or "javascript" in content.lower()

    def test_agents_document_model_validation(self):
        """AgentsDocumentモデル検証テスト"""
        # 最小データでの作成
        doc = AgentsDocument(
            title="Test",
            description="Test desc",
            project_overview={},
            setup_instructions={},
            build_test_instructions={},
            coding_standards={},
            pr_guidelines={},
            auto_generated_note="",
        )

        assert doc.title == "Test"
        assert doc.description == "Test desc"
        assert doc.auto_generated_note == ""

    def test_missing_output_directory(self, temp_project):
        """出力ディレクトリがない場合のテスト"""
        output_dir = temp_project / "output"
        config = {"output": {"agents_doc": str(output_dir / "AGENTS.md")}}

        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator.generate()

        assert result is True
        assert output_dir.exists()
        assert (output_dir / "AGENTS.md").exists()

    @patch("docgen.utils.outlines_utils.should_use_outlines")
    def test_should_use_outlines_integration(self, mock_should_use, temp_project):
        """should_use_outlines統合テスト"""
        mock_should_use.return_value = True

        config = {"use_outlines": True}
        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator._should_use_outlines()

        mock_should_use.assert_called_once_with(config)
        assert result is True

    def test_create_llm_prompt_with_project_info(self, temp_project):
        """プロジェクト情報付きLLMプロンプト作成テスト"""
        config = {"agents": {"custom_instructions": "Custom rules"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project",
            "dependencies": {"python": ["pytest", "black"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest"],
        }

        prompt = generator._create_llm_prompt(project_info)

        assert "Test project" in prompt
        assert "pytest" in prompt
        assert "black" in prompt
        assert "Custom rules" in prompt

    def test_error_handling_in_generate_method(self, temp_project):
        """generateメソッドのエラーハンドリングテスト"""
        generator = AgentsGenerator(temp_project, ["python"], {})

        # プロジェクト情報収集でエラーを発生させる
        with patch.object(
            generator.collector, "collect", side_effect=Exception("Collection error")
        ):
            result = generator.generate()

            assert result is False
