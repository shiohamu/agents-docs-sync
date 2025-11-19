"""
AgentsGeneratorの追加テスト - カバレッジ向上用
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

    def test_collect_project_info_success(self, temp_project):
        """プロジェクト情報収集成功テスト"""
        # テスト用ファイルを作成
        (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")
        (temp_project / "README.md").write_text("# Test Project\n")

        generator = AgentsGenerator(temp_project, ["python"], {})
        project_info = generator._collect_project_info()

        assert "description" in project_info
        assert "dependencies" in project_info

    def test_collect_project_info_empty(self, temp_project):
        """空プロジェクトの情報収集テスト"""
        generator = AgentsGenerator(temp_project, [], {})
        project_info = generator._collect_project_info()

        assert isinstance(project_info, dict)

    @patch("docgen.utils.outlines_utils.should_use_outlines")
    def test_should_use_outlines_integration(self, mock_should_use):
        """should_use_outlines統合テスト"""
        mock_should_use.return_value = True

        config = {"use_outlines": True}
        generator = AgentsGenerator(Path("/tmp"), ["python"], config)

        result = generator._should_use_outlines()

        mock_should_use.assert_called_once_with(config)
        assert result is True

    def test_create_agents_prompt_with_dependencies(self, temp_project):
        """依存関係付きプロンプト作成テスト"""
        config = {"agents": {"custom_instructions": "Custom rules"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project",
            "dependencies": {
                "python": ["pytest", "black"],
                "javascript": ["jest", "eslint"],
            },
            "build_commands": ["npm run build"],
            "test_commands": ["pytest"],
        }

        prompt = generator._create_agents_prompt(project_info)

        assert "Test project" in prompt
        assert "pytest" in prompt
        assert "jest" in prompt
        assert "npm run build" in prompt
        assert "Custom rules" in prompt

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
        assert "jest" in result
        assert "npm run build" in result

    @patch(
        "docgen.generators.agents_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_with_llm_invalid_json(self, mock_create_client, temp_project):
        """無効JSONを返すLLM生成テスト"""
        mock_client = Mock()
        mock_client.generate.return_value = "Invalid JSON response"
        mock_create_client.return_value = mock_client

        generator = AgentsGenerator(
            temp_project, ["python"], {"agents": {"llm_mode": "api"}}
        )

        result = generator._generate_with_llm({})

        assert result is None

    @patch(
        "docgen.generators.agents_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_with_llm_exception(self, mock_create_client, temp_project):
        """LLM生成例外テスト"""
        mock_client = Mock()
        mock_client.generate.side_effect = Exception("LLM error")
        mock_create_client.return_value = mock_client

        generator = AgentsGenerator(
            temp_project, ["python"], {"agents": {"llm_mode": "api"}}
        )

        result = generator._generate_with_llm({})

        assert result is None

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

    def test_generate_hybrid_llm_fallback(self, temp_project):
        """ハイブリッド生成のLLMフォールバックテスト"""
        generator = AgentsGenerator(
            temp_project, ["python"], {"agents": {"llm_mode": "both"}}
        )

        project_info = {"description": "Test project"}

        with patch.object(generator, "_generate_template", return_value=None):
            with patch.object(
                generator, "_generate_with_llm", return_value="LLM content"
            ):
                result = generator._generate_hybrid(project_info)

                assert result == "LLM content"

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

    @patch("docgen.utils.outlines_utils.create_outlines_model")
    @patch("docgen.utils.outlines_utils.should_use_outlines")
    def test_create_outlines_model_integration(
        self, mock_should_use, mock_create_model, temp_project
    ):
        """Outlinesモデル作成統合テスト"""
        mock_should_use.return_value = True
        mock_model = Mock()
        mock_create_model.return_value = mock_model

        config = {"use_outlines": True, "agents": {"llm_mode": "api"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator._create_outlines_model()

        mock_create_model.assert_called_once()
        assert result == mock_model

    def test_write_output_file_creation(self, temp_project):
        """出力ファイル作成テスト"""
        output_path = temp_project / "test_agents.md"
        generator = AgentsGenerator(temp_project, ["python"], {})
        generator.output_path = output_path

        content = "# Test AGENTS Document\n\nThis is a test."

        generator._write_output_file(content)

        assert output_path.exists()
        assert output_path.read_text(encoding="utf-8") == content

    def test_write_output_file_overwrite(self, temp_project):
        """出力ファイル上書きテスト"""
        output_path = temp_project / "test_agents.md"
        output_path.write_text("Original content", encoding="utf-8")

        generator = AgentsGenerator(temp_project, ["python"], {})
        generator.output_path = output_path

        content = "# Updated AGENTS Document\n\nThis is updated."

        generator._write_output_file(content)

        assert output_path.read_text(encoding="utf-8") == content

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

    def test_error_handling_in_generation(self, temp_project):
        """生成時のエラーハンドリングテスト"""
        generator = AgentsGenerator(temp_project, ["python"], {})

        # プロジェクト情報収集でエラーを発生させる
        with patch.object(
            generator,
            "_collect_project_info",
            side_effect=Exception("Collection error"),
        ):
            result = generator.generate()

            assert result is False

    def test_missing_output_directory(self, temp_project):
        """出力ディレクトリがない場合のテスト"""
        output_dir = temp_project / "output"
        config = {"output": {"agents_doc": str(output_dir / "AGENTS.md")}}

        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator.generate()

        assert result is True
        assert output_dir.exists()
        assert (output_dir / "AGENTS.md").exists()
