"""
AgentsGeneratorのテスト
"""

from pathlib import Path

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.generators.agents_generator import AgentsGenerator


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


def test_agents_generator_with_empty_config(temp_project):
    """空の設定でのテスト"""
    config = {}
    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    # デフォルト設定で動作するはず
    assert result is True
    assert (temp_project / "AGENTS.md").exists()


def test_agents_generator_multiple_languages(temp_project):
    """複数言語のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "api"}}

    generator = AgentsGenerator(temp_project, ["python", "javascript"], config)
    result = generator.generate()

    assert result is True
    content = (temp_project / "AGENTS.md").read_text(encoding="utf-8")
    assert "# AGENTS ドキュメント" in content


def test_agents_generator_output_path(temp_project):
    """出力パス指定のテスト"""
    custom_path = "custom/agents.md"
    config = {"output": {"agents_doc": custom_path}, "agents": {"llm_mode": "api"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    result = generator.generate()

    assert result is True
    assert (temp_project / custom_path).exists()
