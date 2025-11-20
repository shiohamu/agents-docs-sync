"""
AgentsGeneratorのテスト
"""

# conftest.pyで.docgenがsys.pathに追加されているため、
# generators.agents_generatorから直接インポート可能
from generators.agents_generator import AgentsGenerator  # pyright: ignore[reportMissingImports]


def test_agents_generator_initialization(temp_project):
    """AgentsGeneratorの初期化テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}
    generator = AgentsGenerator(temp_project, ["python"], config)
    assert generator.project_root == temp_project
    assert generator.languages == ["python"]


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
        "agents": {"llm_mode": "local", "local": {"provider": "ollama", "model": "llama3"}},
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
