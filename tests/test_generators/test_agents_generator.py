"""
AgentsGeneratorのテスト
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# conftest.pyでdocgenがsys.pathに追加されているため、
# generators.agents_generatorから直接インポート可能
from generators.agents_generator import AgentsGenerator, AgentsDocument  # pyright: ignore[reportMissingImports]


def test_agents_generator_initialization(temp_project):
    """AgentsGeneratorの初期化テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator.project_root == temp_project
    assert generator.languages == ["python"]

    def test_initialization(self, agents_generator):
        """AgentsGeneratorの初期化テスト"""
        assert agents_generator.project_root.exists()
        assert agents_generator.languages == ["python"]
        assert hasattr(agents_generator, "config")

def test_generate_agents_md(temp_project):
    """AGENTS.md生成テスト"""
    # テスト用のファイルを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n")
    (temp_project / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n")

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "llm_mode": "both",
            "api": {"provider": "openai"},
            "local": {"provider": "ollama", "model": "llama3"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    assert (temp_project / "AGENTS.md").exists()

    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "# AGENTS ドキュメント" in content
    assert "開発環境のセットアップ" in content
    assert "ビルドおよびテスト手順" in content
    assert "APIを使用する場合" in content
    assert "ローカルLLMを使用する場合" in content


def test_should_use_outlines_enabled(temp_project):
    """Outlines使用判定テスト - 有効"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "use_outlines": True}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator._should_use_outlines() is True


def test_should_use_outlines_disabled(temp_project):
    """Outlines使用判定テスト - 無効"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "use_outlines": False}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator._should_use_outlines() is False


def test_should_use_outlines_default(temp_project):
    """Outlines使用判定テスト - デフォルト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator._should_use_outlines() is False


def test_agents_document_creation():
    """AgentsDocumentの作成テスト"""
    data = {
        "title": "Test Document",
        "description": "Test description",
        "project_overview": {"name": "test"},
        "setup_instructions": {"prerequisites": ["Python 3.12"]},
        "build_test_instructions": {"build_commands": ["python setup.py build"]},
        "coding_standards": {"standards": ["Use PEP 8"]},
        "pr_guidelines": {"branch_creation": "git checkout -b feature/branch"},
        "auto_generated_note": "Auto-generated document",
    }

    doc = AgentsDocument(**data)
    assert doc.title == "Test Document"
    assert doc.description == "Test description"
    assert doc.project_overview == {"name": "test"}
    assert doc.setup_instructions == {"prerequisites": ["Python 3.12"]}
    assert doc.build_test_instructions == {"build_commands": ["python setup.py build"]}
    assert doc.coding_standards == {"standards": ["Use PEP 8"]}
    assert doc.pr_guidelines == {"branch_creation": "git checkout -b feature/branch"}
    assert doc.auto_generated_note == "Auto-generated document"


def test_convert_structured_data_to_markdown(temp_project):
    """構造化データからマークダウン変換テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    data = AgentsDocument(
        title="Test Document",
        description="Test description",
        project_overview={"name": "test"},
        setup_instructions={"prerequisites": ["Python 3.12"]},
        build_test_instructions={"build_commands": ["python setup.py build"]},
        coding_standards={"standards": ["Use PEP 8"]},
        pr_guidelines={"branch_creation": "git checkout -b feature/branch"},
        auto_generated_note="Auto-generated document",
    )

    project_info = {}
    markdown = generator._convert_structured_data_to_markdown(data, project_info)

    assert "# Test Document" in markdown
    assert "Test description" in markdown
    assert "Python 3.12" in markdown
    assert "python setup.py build" in markdown
    assert "Use PEP 8" in markdown
    assert "Auto-generated document" in markdown


@patch("utils.outlines_utils.OUTLINES_AVAILABLE", True)
def test_generate_with_outlines_success(temp_project):
    """Outlines生成成功テスト"""
    from unittest.mock import Mock

    # Mock Outlines
    mock_model = Mock()
    mock_model.return_value = AgentsDocument(
        title="Test Document",
        description="Test description",
        project_overview={"name": "test"},
        setup_instructions={"prerequisites": ["Python 3.12"]},
        build_test_instructions={"build_commands": ["python setup.py build"]},
        coding_standards={"standards": ["Use PEP 8"]},
        pr_guidelines={"branch_creation": "git checkout -b feature/branch"},
        auto_generated_note="Auto-generated document",
    )

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "use_outlines": True,
        "agents": {"llm_mode": "api", "api": {"provider": "openai", "model": "gpt-4o"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)

    with patch.object(generator, "_create_outlines_model", return_value=mock_model):
        result = generator._generate_with_outlines({})

        assert result is not None
        assert "# Test Document" in result
        assert "Test description" in result


@patch("utils.outlines_utils.OUTLINES_AVAILABLE", False)
def test_generate_with_outlines_fallback(temp_project):
    """Outlines生成フォールバックテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "use_outlines": True,
        "agents": {"llm_mode": "api"},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator._generate_with_outlines({})

    # Outlinesが利用できないため、従来の生成にフォールバック
    assert result is not None
    assert "# AGENTS ドキュメント" in result


def test_llm_mode_api_only(temp_project):
    """llm_mode: 'api' の場合のテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"llm_mode": "api", "api": {"provider": "openai"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "APIを使用する場合" in content
    assert "ローカルLLMを使用する場合" not in content


def test_llm_mode_local_only(temp_project):
    """llm_mode: 'local' の場合のテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "llm_mode": "local",
            "local": {"provider": "ollama", "model": "llama3"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "APIを使用する場合" not in content
    assert "ローカルLLMを使用する場合" in content


def test_custom_instructions(temp_project):
    """カスタム指示のテスト"""
    custom_instructions = (
        "- すべての関数にはdocstringを記述すること\n- テストカバレッジは80%以上を維持すること"
    )

    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"llm_mode": "both", "custom_instructions": custom_instructions},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "プロジェクト固有の指示" in content
    assert "docstringを記述すること" in content
    assert "テストカバレッジは80%以上" in content


def test_anthropic_provider(temp_project):
    """Anthropicプロバイダーのテスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "llm_mode": "api",
            "api": {"provider": "anthropic", "api_key_env": "ANTHROPIC_API_KEY"},
        },
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "Anthropic APIキーを取得" in content
    assert "ANTHROPIC_API_KEY" in content


def test_no_agents_config(temp_project):
    """agentsセクションがない場合のテスト（デフォルト動作）"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    # デフォルトではbothなので両方のセクションが表示される
    assert "APIを使用する場合" in content
    assert "ローカルLLMを使用する場合" in content


def test_no_build_commands(temp_project):
    """ビルドコマンドがない場合のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    # ビルドコマンドがない場合は適切なメッセージが表示される
    assert "ビルド手順は設定されていません" in content or "ビルド手順" in content

    def test_generate_markdown_template_mode(self, temp_project):
        """マークダウン生成 - templateモードのテスト"""
        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {"generation": {"agents_mode": "template"}},
        }
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project",
            "dependencies": {"python": ["pytest"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest"],
        }

        result = generator._generate_markdown(project_info)

        assert "# AGENTS ドキュメント" in result
        assert "Test project" in result
        assert "pytest" in result

    def test_generate_markdown_llm_mode(self, temp_project):
        """マークダウン生成 - llmモードのテスト"""
        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {"generation": {"agents_mode": "llm"}},
        }
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {"description": "Test project"}

        with patch.object(
            generator, "_generate_with_llm", return_value="LLM generated content"
        ):
            result = generator._generate_markdown(project_info)

        assert result == "LLM generated content"

    def test_generate_markdown_hybrid_mode(self, temp_project):
        """マークダウン生成 - hybridモードのテスト"""
        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {"generation": {"agents_mode": "hybrid"}},
        }
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {"description": "Test project"}

        with patch.object(
            generator, "_generate_hybrid", return_value="Hybrid generated content"
        ):
            result = generator._generate_markdown(project_info)

        assert result == "Hybrid generated content"

    def test_generate_with_llm_success(self, temp_project):
        """LLMを使用した生成成功テスト"""
        config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {"description": "Test project"}

        with patch(
            "generators.agents_generator.LLMClientFactory.create_client_with_fallback"
        ) as mock_create_client:
            mock_client = Mock()
            mock_client.generate.return_value = '{"title": "Test", "description": "Test project", "project_overview": {"name": "test"}, "setup_instructions": {}, "build_test_instructions": {}, "coding_standards": {}, "pr_guidelines": {}, "auto_generated_note": ""}'
            mock_create_client.return_value = mock_client

            result = generator._generate_with_llm(project_info)

            assert result is not None
            assert "# Test" in result

    def test_generate_with_llm_no_client(self, temp_project):
        """LLMクライアントなしの場合のテスト"""
        config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {"description": "Test project"}

        with patch(
            "generators.agents_generator.LLMClientFactory.create_client_with_fallback",
            return_value=None,
        ):
            result = generator._generate_with_llm(project_info)

            assert result is None

    def test_generate_hybrid_success(self, temp_project):
        """ハイブリッド生成成功テスト"""
        config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {"description": "Test project"}

        with patch.object(
            generator, "_generate_template", return_value="Template content"
        ):
            with patch.object(
                generator, "_generate_with_llm", return_value="LLM content"
            ):
                result = generator._generate_hybrid(project_info)

                assert result is not None
                assert "Template content" in result
                assert "LLM content" in result

    def test_create_agents_prompt(self, temp_project):
        """AGENTSプロンプト作成テスト"""
        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {
                "llm_mode": "both",
                "custom_instructions": "Custom instructions",
            },
        }
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project",
            "dependencies": {"python": ["pytest"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest"],
        }

        result = generator._create_agents_prompt(project_info)

        assert "Test project" in result
        assert "pytest" in result
        assert "Custom instructions" in result
        assert "Conventional Commits" in result

    def test_convert_structured_data_to_markdown(self, temp_project):
        """構造化データをマークダウンに変換テスト"""
        config = {}
        generator = AgentsGenerator(temp_project, ["python"], config)

        data = {
            "title": "Test Document",
            "description": "Test description",
            "project_overview": {"name": "test"},
            "setup_instructions": {"prerequisites": ["Python 3.8+"]},
            "build_test_instructions": {"build_commands": ["python setup.py build"]},
            "coding_standards": {"standards": ["Use PEP 8"]},
            "pr_guidelines": {"branch_creation": "git checkout -b feature/branch"},
            "auto_generated_note": "Auto-generated document",
        }

        result = generator._convert_structured_data_to_markdown(data)

        assert "# Test Document" in result
        assert "Test description" in result
        assert "Python 3.8+" in result
        assert "python setup.py build" in result
        assert "Use PEP 8" in result
        assert "git checkout -b feature/branch" in result

    def test_generate_template_success(self, temp_project):
        """テンプレート生成成功テスト"""
        config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}
        generator = AgentsGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project",
            "dependencies": {"python": ["pytest"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest"],
        }

        result = generator._generate_template(project_info)

        assert "# AGENTS ドキュメント" in result
        assert "Test project" in result
        assert "pytest" in result
        assert "python setup.py build" in result

    @patch("generators.agents_generator.LLMClientFactory.create_client_with_fallback")
    def test_generate_with_outlines_success_agents(
        self, mock_create_client, temp_project
    ):
        """Outlinesを使用したAGENTS生成成功テスト"""
        mock_client = Mock()
        mock_client.generate.return_value = '{"title": "Test", "description": "Test project", "project_overview": {"name": "test"}, "setup_instructions": {}, "build_test_instructions": {}, "coding_standards": {}, "pr_guidelines": {}, "auto_generated_note": ""}'
        mock_create_client.return_value = mock_client

        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "use_outlines": True,
            "agents": {"llm_mode": "api"},
        }
        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator._generate_with_outlines({})

        assert result is not None
        assert "# Test" in result
        assert "Test project" in result

    @patch("generators.agents_generator.LLMClientFactory.create_client_with_fallback")
    def test_generate_with_outlines_fallback_agents(
        self, mock_create_client, temp_project
    ):
        """Outlines生成失敗時のフォールバックテスト（AGENTS）"""
        mock_create_client.return_value = None

        config = {"output": {"agents_doc": "AGENTS.md"}, "use_outlines": True}
        generator = AgentsGenerator(temp_project, ["python"], config)

        result = generator._generate_with_outlines({})

        assert result is not None  # フォールバック生成が動作
