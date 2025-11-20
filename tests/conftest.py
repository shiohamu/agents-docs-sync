"""
pytest設定と共通フィクスチャ
"""

from pathlib import Path
import sys

import pytest

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(DOCGEN_DIR))


@pytest.fixture
def temp_project(tmp_path):
    """
    テスト用の一時プロジェクトディレクトリを作成

    Returns:
        Path: 一時プロジェクトのルートディレクトリ
    """
    project_root = tmp_path / "test_project"
    project_root.mkdir()
    return project_root


@pytest.fixture
def sample_python_file(temp_project):
    """
    サンプルPythonファイル（docstring付き関数）を作成

    Returns:
        Path: 作成されたPythonファイルのパス
    """
    code = '''"""
サンプルモジュール
"""

def hello_world(name: str) -> str:
    """
    挨拶を返す関数

    Args:
        name: 名前

    Returns:
        挨拶メッセージ
    """
    return f"Hello, {name}!"

class SampleClass:
    """
    サンプルクラス
    """

    def __init__(self, value: int):
        """
        初期化

        Args:
            value: 初期値
        """
        self.value = value

    def get_value(self) -> int:
        """値を取得"""
        return self.value
'''
    file_path = temp_project / "sample.py"
    file_path.write_text(code, encoding="utf-8")
    return file_path


@pytest.fixture
def sample_javascript_file(temp_project):
    """
    サンプルJavaScriptファイル（JSDoc付き関数）を作成

    Returns:
        Path: 作成されたJavaScriptファイルのパス
    """
    code = """/**
 * サンプルモジュール
 */

/**
 * 挨拶を返す関数
 * @param {string} name - 名前
 * @returns {string} 挨拶メッセージ
 */
function helloWorld(name) {
    return `Hello, ${name}!`;
}

/**
 * サンプルクラス
 */
class SampleClass {
    /**
     * コンストラクタ
     * @param {number} value - 初期値
     */
    constructor(value) {
        this.value = value;
    }

    /**
     * 値を取得
     * @returns {number} 値
     */
    getValue() {
        return this.value;
    }
}
"""
    file_path = temp_project / "sample.js"
    file_path.write_text(code, encoding="utf-8")
    return file_path


@pytest.fixture
def sample_config(temp_project):
    """
    サンプル設定ファイルを作成

    Returns:
        Path: 作成された設定ファイルのパス
    """
    config = {
        "languages": {"auto_detect": True, "preferred": []},
        "output": {"api_doc": "docs/api.md", "readme": "README.md"},
        "generation": {
            "update_readme": True,
            "generate_api_doc": True,
            "preserve_manual_sections": True,
        },
    }

    import yaml

    config_dir = temp_project / ".docgen"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)

    return config_path


@pytest.fixture
def python_project(temp_project):
    """
    Pythonプロジェクトの構造を作成

    Returns:
        Path: プロジェクトルート
    """
    # requirements.txt
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n", encoding="utf-8")

    # サンプルPythonファイル
    (temp_project / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")

    return temp_project


@pytest.fixture
def javascript_project(temp_project):
    """
    JavaScriptプロジェクトの構造を作成

    Returns:
        Path: プロジェクトルート
    """
    # package.json
    import json

    package_json = {
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {"express": "^4.18.0"},
    }
    (temp_project / "package.json").write_text(json.dumps(package_json, indent=2), encoding="utf-8")

    # サンプルJavaScriptファイル
    (temp_project / "index.js").write_text('console.log("Hello");\n', encoding="utf-8")

    return temp_project


@pytest.fixture
def go_project(temp_project):
    """
    Goプロジェクトの構造を作成

    Returns:
        Path: プロジェクトルート
    """
    # go.mod
    (temp_project / "go.mod").write_text("module test-project\n\ngo 1.20\n", encoding="utf-8")

    # サンプルGoファイル
    (temp_project / "main.go").write_text("package main\n\nfunc main() {\n}\n", encoding="utf-8")

    return temp_project


@pytest.fixture
def multi_language_project(temp_project):
    """
    複数言語プロジェクトの構造を作成

    Returns:
        Path: プロジェクトルート
    """
    # Python
    (temp_project / "requirements.txt").write_text("pytest>=7.0.0\n", encoding="utf-8")
    (temp_project / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")

    # JavaScript
    import json

    (temp_project / "package.json").write_text(
        json.dumps({"name": "test-project"}, indent=2), encoding="utf-8"
    )
    (temp_project / "index.js").write_text('console.log("Hello");\n', encoding="utf-8")

    return temp_project


@pytest.fixture
def default_config():
    """
    デフォルトの設定オブジェクトを返す

    Returns:
        dict: デフォルト設定
    """
    return {
        "languages": {"auto_detect": True, "preferred": []},
        "output": {"api_doc": "docs/api.md", "readme": "README.md", "agents_doc": "AGENTS.md"},
        "generation": {
            "update_readme": True,
            "generate_api_doc": True,
            "generate_agents_doc": True,
            "preserve_manual_sections": True,
        },
        "agents": {
            "llm_mode": "both",
            "api": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
            "local": {"provider": "ollama", "model": "llama3"},
        },
    }


@pytest.fixture
def agents_config():
    """
    AGENTSドキュメント生成用の設定を返す

    Returns:
        dict: AGENTS設定
    """
    return {
        "output": {"agents_doc": "AGENTS.md"},
        "agents": {
            "llm_mode": "both",
            "api": {"provider": "openai", "api_key_env": "OPENAI_API_KEY"},
            "local": {"provider": "ollama", "model": "llama3"},
        },
    }


@pytest.fixture
def api_config():
    """
    APIドキュメント生成用の設定を返す

    Returns:
        dict: API設定
    """
    return {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}


@pytest.fixture
def readme_config():
    """
    README生成用の設定を返す

    Returns:
        dict: README設定
    """
    return {
        "output": {"readme": "README.md"},
        "generation": {"update_readme": True, "preserve_manual_sections": True},
    }


@pytest.fixture
def agents_generator(temp_project, agents_config):
    """
    AgentsGeneratorインスタンスを作成

    Returns:
        AgentsGenerator: 初期化されたジェネレーター
    """
    from docgen.generators.agents_generator import AgentsGenerator

    return AgentsGenerator(temp_project, ["python"], agents_config)


@pytest.fixture
def api_generator(temp_project, api_config):
    """
    APIGeneratorインスタンスを作成

    Returns:
        APIGenerator: 初期化されたジェネレーター
    """
    from docgen.generators.api_generator import APIGenerator

    return APIGenerator(temp_project, ["python"], api_config)


@pytest.fixture
def readme_generator(temp_project, readme_config):
    """
    ReadmeGeneratorインスタンスを作成

    Returns:
        ReadmeGenerator: 初期化されたジェネレーター
    """
    from docgen.generators.readme_generator import ReadmeGenerator

    return ReadmeGenerator(temp_project, ["python"], readme_config)


@pytest.fixture
def config_manager(temp_project, default_config):
    """
    ConfigManagerインスタンスを作成

    Returns:
        ConfigManager: 初期化された設定マネージャー
    """
    from docgen.config_manager import ConfigManager

    return ConfigManager(temp_project, temp_project)


@pytest.fixture
def project_info_collector(temp_project):
    """
    ProjectInfoCollectorインスタンスを作成

    Returns:
        ProjectInfoCollector: 初期化された情報収集器
    """
    from docgen.collectors.project_info_collector import ProjectInfoCollector

    return ProjectInfoCollector(temp_project)
