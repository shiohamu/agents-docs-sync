"""
AgentsGeneratorのテスト
"""

import pytest

from docgen.generators.agents_generator import AgentsGenerator
from tests.test_utils import assert_file_contains_text, assert_file_exists_and_not_empty


class TestAgentsGenerator:
    """AgentsGeneratorのテストクラス"""

    def test_initialization(self, agents_generator):
        """AgentsGeneratorの初期化テスト"""
        assert agents_generator.project_root.exists()
        assert agents_generator.languages == ["python"]
        assert hasattr(agents_generator, "config")

    def test_generate_agents_md(self, agents_generator, python_project):
        """AGENTS.md生成テスト"""
        result = agents_generator.generate()

        assert result is True
        agents_doc_path = agents_generator.output_path
        assert_file_exists_and_not_empty(agents_doc_path)

        assert_file_contains_text(
            agents_doc_path,
            "# AGENTS ドキュメント",
            "開発環境のセットアップ",
            "ビルドおよびテスト手順",
            "APIを使用する場合",
            "ローカルLLMを使用する場合",
        )

    @pytest.mark.parametrize(
        "llm_mode,expected_api,expected_local",
        [
            ("both", True, True),
            ("api", True, False),
            ("local", False, True),
        ],
    )
    def test_llm_mode_configurations(self, temp_project, llm_mode, expected_api, expected_local):
        """LLMモード別の設定テスト"""
        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {
                "llm_mode": llm_mode,
                "api": {"provider": "openai"},
                "local": {"provider": "ollama", "model": "llama3"},
            },
        }

        generator = AgentsGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        content = generator.output_path.read_text(encoding="utf-8")

        if expected_api:
            assert "APIを使用する場合" in content
        else:
            assert "APIを使用する場合" not in content

        if expected_local:
            assert "ローカルLLMを使用する場合" in content
        else:
            assert "ローカルLLMを使用する場合" not in content


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


def test_generate_project_overview_section(temp_project):
    """プロジェクト概要セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_project_overview({})

    assert isinstance(lines, list)
    assert len(lines) > 0
    assert "プロジェクト概要" in "\n".join(lines)


def test_generate_setup_section(temp_project):
    """セットアップセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_setup_section({})

    assert isinstance(lines, list)
    assert "## 開発環境のセットアップ" in "\n".join(lines)


def test_generate_prerequisites_section(temp_project):
    """前提条件セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_prerequisites_section()

    assert isinstance(lines, list)
    assert "### 前提条件" in "\n".join(lines)
    assert "Python 3.12以上" in "\n".join(lines)


def test_generate_dependencies_section(temp_project):
    """依存関係セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_dependencies_section({})

    assert isinstance(lines, list)
    assert "### 依存関係のインストール" in "\n".join(lines)


def test_generate_python_dependencies(temp_project):
    """Python依存関係セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    # requirements.txtを作成
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n", encoding="utf-8")

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_python_dependencies()

    assert isinstance(lines, list)
    assert "#### Python依存関係" in "\n".join(lines)
    assert "pip install -r requirements.txt" in "\n".join(lines)


def test_generate_nodejs_dependencies(temp_project):
    """Node.js依存関係セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["javascript"], config)
    lines = generator._generate_nodejs_dependencies()

    assert isinstance(lines, list)
    assert "#### Node.js依存関係" in "\n".join(lines)
    assert "npm install" in "\n".join(lines)


def test_generate_api_setup_section(temp_project):
    """APIセットアップセクションの生成テスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"api": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_api_setup_section()

    assert isinstance(lines, list)
    assert "#### APIを使用する場合" in "\n".join(lines)
    assert "OPENAI_API_KEY" in "\n".join(lines)


def test_generate_local_setup_section(temp_project):
    """ローカルLLMセットアップセクションの生成テスト"""
    config = {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {"local": {"provider": "ollama", "model": "llama3"}},
    }

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_local_setup_section()

    assert isinstance(lines, list)
    assert "#### ローカルLLMを使用する場合" in "\n".join(lines)
    assert "ollama pull llama3" in "\n".join(lines)


def test_generate_build_section(temp_project):
    """ビルドセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_build_section({}, False)

    assert isinstance(lines, list)
    assert "### ビルド手順" in "\n".join(lines)


def test_generate_test_section(temp_project):
    """テストセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_test_section({}, False)

    assert isinstance(lines, list)
    assert "### テスト実行" in "\n".join(lines)


def test_generate_test_commands_by_mode(temp_project):
    """LLMモード別のテストコマンド生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_test_commands_by_mode(["pytest tests/"])

    assert isinstance(lines, list)
    assert "#### APIを使用する場合" in "\n".join(lines)
    assert "#### ローカルLLMを使用する場合" in "\n".join(lines)


def test_generate_default_test_commands(temp_project):
    """デフォルトテストコマンド生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}, "agents": {"llm_mode": "both"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_default_test_commands()

    assert isinstance(lines, list)
    assert "uv run pytest tests/" in "\n".join(lines)


def test_generate_coding_standards_section(temp_project):
    """コーディング規約セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_coding_standards_section({})

    assert isinstance(lines, list)
    assert "## コーディング規約" in "\n".join(lines)


def test_generate_formatter_section(temp_project):
    """フォーマッターセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_formatter_section({"formatter": "black"})

    assert isinstance(lines, list)
    assert "### フォーマッター" in "\n".join(lines)
    assert "black" in "\n".join(lines)


def test_generate_linter_section(temp_project):
    """リンターセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_linter_section({"linter": "ruff"})

    assert isinstance(lines, list)
    assert "### リンター" in "\n".join(lines)
    assert "ruff" in "\n".join(lines)


def test_generate_style_guide_section(temp_project):
    """スタイルガイドセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_style_guide_section({"style_guide": "PEP 8"})

    assert isinstance(lines, list)
    assert "### スタイルガイド" in "\n".join(lines)
    assert "PEP 8" in "\n".join(lines)


def test_get_formatter_commands(temp_project):
    """フォーマッターコマンド取得テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)

    # blackの場合
    commands = generator._get_formatter_commands("black")
    assert "black ." in str(commands)

    # prettierの場合
    commands = generator._get_formatter_commands("prettier")
    assert "prettier" in str(commands)

    # 未知のフォーマッターの場合
    commands = generator._get_formatter_commands("unknown")
    assert commands == []


def test_get_linter_commands(temp_project):
    """リンターコマンド取得テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)

    # ruffの場合
    commands = generator._get_linter_commands("ruff")
    assert "ruff check ." in str(commands)
    assert "ruff format ." in str(commands)

    # 未知のリンターの場合
    commands = generator._get_linter_commands("unknown")
    assert commands == []


def test_generate_pr_section(temp_project):
    """PRセクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_pr_section({})

    assert isinstance(lines, list)
    assert "## プルリクエストの手順" in "\n".join(lines)
    assert "git checkout -b" in "\n".join(lines)


def test_generate_custom_instructions_section(temp_project):
    """カスタム指示セクションの生成テスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}

    generator = AgentsGenerator(temp_project, ["python"], config)
    lines = generator._generate_custom_instructions_section("テスト指示")

    assert isinstance(lines, list)
    assert "## プロジェクト固有の指示" in "\n".join(lines)
    assert "テスト指示" in "\n".join(lines)


def test_agents_generator_has_uv_config_with_uv(temp_project):
    """uv設定がある場合のテスト"""
    pyproject_content = """[tool.uv]
dev-dependencies = ["pytest"]
"""
    (temp_project / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    config = {"output": {"agents_doc": "AGENTS.md"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    assert generator._has_uv_config() is True


def test_agents_generator_has_uv_config_without_uv(temp_project):
    """uv設定がない場合のテスト"""
    pyproject_content = """[tool.black]
line-length = 88
"""
    (temp_project / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    config = {"output": {"agents_doc": "AGENTS.md"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    assert generator._has_uv_config() is False


def test_agents_generator_has_uv_config_no_pyproject(temp_project):
    """pyproject.tomlが存在しない場合のテスト"""
    config = {"output": {"agents_doc": "AGENTS.md"}}
    generator = AgentsGenerator(temp_project, ["python"], config)

    assert generator._has_uv_config() is False
