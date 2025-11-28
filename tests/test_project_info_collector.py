"""
ProjectInfoCollectorのテスト
"""

from pathlib import Path
from unittest.mock import patch

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.collectors.project_info_collector import ProjectInfoCollector


class TestProjectInfoCollector:
    """ProjectInfoCollectorクラスのテスト"""

    def test_project_info_collector_initialization(self, temp_project):
        """ProjectInfoCollectorの初期化テスト"""
        collector = ProjectInfoCollector(temp_project)

        assert collector.project_root == temp_project

    def test_project_info_collector_initialization_with_package_managers(self, temp_project):
        """パッケージマネージャ付き初期化テスト"""
        package_managers = {"python": "uv", "javascript": "npm"}
        collector = ProjectInfoCollector(temp_project, package_managers)

        assert collector.project_root == temp_project
        assert collector.package_managers == package_managers

    def test_collect_all(self, temp_project):
        """全情報収集テスト"""
        collector = ProjectInfoCollector(temp_project)

        with patch.object(collector, "collect_project_description", return_value="Test project"):
            with patch.object(
                collector.build_collector, "collect_build_commands", return_value=["make build"]
            ):
                with patch.object(collector, "collect_test_commands", return_value=["make test"]):
                    with patch.object(
                        collector, "collect_dependencies", return_value={"python": ["pytest"]}
                    ):
                        with patch.object(
                            collector,
                            "collect_coding_standards",
                            return_value={"formatter": "black"},
                        ):
                            with patch.object(
                                collector,
                                "collect_ci_cd_info",
                                return_value={"github_actions": True},
                            ):
                                with patch.object(
                                    collector,
                                    "collect_project_structure",
                                    return_value={"directories": ["src"], "files": ["main.py"]},
                                ):
                                    result = collector.collect_all()

                                    from docgen.models import ProjectInfo

                                    expected = ProjectInfo(
                                        description="Test project",
                                        build_commands=["make build"],
                                        test_commands=["make test"],
                                        dependencies={"python": ["pytest"]},
                                        coding_standards={"formatter": "black"},
                                        ci_cd_info={"github_actions": True},
                                        project_structure={
                                            "directories": ["src"],
                                            "files": ["main.py"],
                                        },
                                        key_features=[],
                                    )

                                    assert result == expected

    def test_collect_build_commands_from_pipeline_script(self, temp_project):
        """パイプラインスクリプトからのビルドコマンド収集テスト"""
        scripts_dir = temp_project / "scripts"
        scripts_dir.mkdir()
        pipeline_script = scripts_dir / "run_pipeline.sh"
        pipeline_script.write_text("""
#!/bin/bash
echo "Building project..."
make build
npm run build
python setup.py build
        """)

        collector = ProjectInfoCollector(temp_project)
        commands = collector.build_collector.collect_build_commands()

        assert "make build" in commands
        assert "npm run build" in commands
        assert "python setup.py build" in commands

    def test_collect_build_commands_with_package_managers(self, temp_project):
        """パッケージマネージャ考慮のビルドコマンド収集テスト"""
        # Pythonプロジェクト
        collector = ProjectInfoCollector(temp_project, {"python": "uv"})
        commands = collector.build_collector.collect_build_commands()
        # uvプロジェクトでは特別なビルドコマンドは追加されない

        # JavaScriptプロジェクト
        collector = ProjectInfoCollector(temp_project, {"javascript": "pnpm"})
        package_json = temp_project / "package.json"
        package_json.write_text('{"scripts": {"build": "webpack"}}')
        commands = collector.build_collector.collect_build_commands()
        assert "pnpm run build" in commands

        # Goプロジェクト
        collector = ProjectInfoCollector(temp_project, {"go": "go"})
        commands = collector.build_collector.collect_build_commands()
        assert "go build" in commands

    def test_collect_build_commands_from_makefile(self, temp_project):
        """Makefileからのビルドコマンド収集テスト"""
        makefile = temp_project / "Makefile"
        makefile.write_text("""
.PHONY: build test clean

build:
\t@echo "Building..."
\tgcc main.c -o main
\tgo build -o bin/app .

test:
\t@echo "Testing..."
\tgo test ./...

clean:
\t@echo "Cleaning..."
\trm -rf bin/
        """)

        collector = ProjectInfoCollector(temp_project)
        commands = collector.build_collector.collect_build_commands()

        assert "gcc main.c -o main" in commands
        assert "go build -o bin/app ." in commands

    def test_collect_build_commands_from_package_json(self, temp_project):
        """package.jsonからのビルドコマンド収集テスト"""
        package_json = temp_project / "package.json"
        package_json.write_text("""
{
  "name": "test-project",
  "scripts": {
    "build": "webpack --mode production",
    "compile": "tsc",
    "package": "npm pack"
  }
}
        """)

        collector = ProjectInfoCollector(temp_project)
        commands = collector.build_collector.collect_build_commands()

        assert "npm run build" in commands
        assert "npm run compile" in commands

    def test_collect_test_commands_from_makefile(self, temp_project):
        """Makefileからのテストコマンド収集テスト"""
        makefile = temp_project / "Makefile"
        makefile.write_text("""
test:
\tpytest tests/
\tgo test ./...
\tnpm test

integration-test:
\tdocker-compose up -d
\tpytest tests/integration/
""")

        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_test_commands()

        assert "pytest tests/" in commands
        assert "go test ./..." in commands
        assert "npm test" in commands

    def test_collect_test_commands_with_package_managers(self, temp_project):
        """パッケージマネージャ考慮のテストコマンド収集テスト"""
        # Pythonプロジェクト (uv)
        collector = ProjectInfoCollector(temp_project, {"python": "uv"})
        commands = collector.collect_test_commands()
        assert "uv run pytest tests/ -v --tb=short" in commands

        # Poetryプロジェクト
        collector = ProjectInfoCollector(temp_project, {"python": "poetry"})
        commands = collector.collect_test_commands()
        assert "poetry run pytest tests/ -v --tb=short" in commands

        # JavaScriptプロジェクト
        collector = ProjectInfoCollector(temp_project, {"javascript": "yarn"})
        package_json = temp_project / "package.json"
        package_json.write_text('{"scripts": {"test": "jest"}}')
        commands = collector.collect_test_commands()
        assert "yarn test" in commands

        # Goプロジェクト
        collector = ProjectInfoCollector(temp_project, {"go": "go"})
        commands = collector.collect_test_commands()
        assert "go test ./..." in commands

    def test_collect_build_commands_with_uv_run(self, temp_project):
        """uvプロジェクトでのpythonコマンドにuv runがつくテスト"""
        # uvプロジェクトでpythonコマンドを含むスクリプト
        scripts_dir = temp_project / "scripts"
        scripts_dir.mkdir()
        pipeline_script = scripts_dir / "run_pipeline.sh"
        pipeline_script.write_text("""
#!/bin/bash
python3 setup.py build
python3 -m pytest tests/
""")

        collector = ProjectInfoCollector(temp_project, {"python": "uv"})
        commands = collector.build_collector.collect_build_commands()

        assert "uv run python3 setup.py build" in commands
        assert "uv run python3 -m pytest tests/" in commands

    def test_collect_test_commands_from_package_json(self, temp_project):
        """package.jsonからのテストコマンド収集テスト"""
        package_json = temp_project / "package.json"
        package_json.write_text("""
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest unit/",
    "test:integration": "jest integration/"
  }
}
""")

        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_test_commands()

        assert "npm test" in commands

    def test_collect_dependencies_from_requirements_txt(self, temp_project):
        """requirements.txtからの依存関係収集テスト"""
        requirements_txt = temp_project / "requirements.txt"
        requirements_txt.write_text("""
pytest>=7.0.0
requests==2.28.1
flask
numpy>=1.21.0,<2.0.0
""")

        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert "python" in dependencies
        python_deps = dependencies["python"]
        assert "pytest>=7.0.0" in python_deps
        assert "requests==2.28.1" in python_deps
        assert "flask" in python_deps
        assert "numpy>=1.21.0,<2.0.0" in python_deps

    def test_collect_dependencies_from_package_json(self, temp_project):
        """package.jsonからの依存関係収集テスト"""
        package_json = temp_project / "package.json"
        package_json.write_text("""
{
  "dependencies": {
    "react": "^18.2.0",
    "lodash": "~4.17.21"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@types/node": "^18.0.0"
  }
}
""")

        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert "nodejs" in dependencies
        nodejs_deps = dependencies["nodejs"]
        assert "react@^18.2.0" in nodejs_deps
        assert "lodash@~4.17.21" in nodejs_deps

    def test_collect_coding_standards_from_pyproject_toml(self, temp_project):
        """pyproject.tomlからのコーディング規約収集テスト"""
        pyproject_toml = temp_project / "pyproject.toml"
        pyproject_toml.write_text("""
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.ruff]
line-length = 88
""")

        collector = ProjectInfoCollector(temp_project)
        standards = collector.collect_coding_standards()

        assert "formatter" in standards
        assert standards["formatter"] == "black"
        assert "import_sorter" in standards
        assert standards["import_sorter"] == "isort"
        assert "linter" in standards
        assert standards["linter"] == "ruff"
        assert any("ruff" in standard.lower() for standard in standards)

    def test_collect_ci_cd_info_github_actions(self, temp_project):
        """GitHub Actions CI/CD情報収集テスト"""
        github_dir = temp_project / ".github" / "workflows"
        github_dir.mkdir(parents=True)
        workflow_file = github_dir / "ci.yml"
        workflow_file.write_text("""
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: make test
""")

        collector = ProjectInfoCollector(temp_project)
        ci_cd_info = collector.collect_ci_cd_info()

        assert "github_actions" in ci_cd_info
        assert "ci.yml" in ci_cd_info["github_actions"]

    def test_collect_project_structure(self, temp_project):
        """プロジェクト構造収集テスト"""
        # ディレクトリ構造を作成
        (temp_project / "src").mkdir()
        (temp_project / "src" / "__init__.py").write_text("")
        (temp_project / "src" / "main.py").write_text("""
class A: pass
class B: pass
class C: pass
def d(): pass
def e(): pass
def f(): pass
""")
        (temp_project / "tests").mkdir()
        (temp_project / "tests" / "test_main.py").write_text("")
        (temp_project / "docs").mkdir()
        (temp_project / "README.md").write_text("# Project")

        collector = ProjectInfoCollector(temp_project)
        structure = collector.collect_project_structure()

        assert "src/" in structure
        assert "tests/" in structure
        assert "docs/" in structure
        assert "README.md" in structure

    def test_collect_project_description_from_readme(self, temp_project):
        """READMEからのプロジェクト説明収集テスト"""
        readme = temp_project / "README.md"
        readme.write_text("""# My Awesome Project

This is a description of my awesome project. It does amazing things and solves real problems.

## Features

- Feature 1
- Feature 2
""")

        collector = ProjectInfoCollector(temp_project)
        description = collector.collect_project_description()

        assert description is not None
        assert "amazing things" in description

    def test_collect_project_description_from_setup_py(self, temp_project):
        """setup.pyからのプロジェクト説明収集テスト"""
        setup_py = temp_project / "setup.py"
        setup_py.write_text("""
from setuptools import setup

setup(
    name="my-project",
    description="A short description",
    long_description="A much longer description of the project that explains what it does and why it's useful.",
    author="Test Author"
)
""")

        collector = ProjectInfoCollector(temp_project)
        description = collector.collect_project_description()

        assert description is not None
        assert "A short description" in description

    def test_collect_project_description_from_package_json(self, temp_project):
        """package.jsonからのプロジェクト説明収集テスト"""
        package_json = temp_project / "package.json"
        package_json.write_text("""
{
  "name": "my-package",
  "description": "A JavaScript package description",
  "version": "1.0.0"
}
""")

        collector = ProjectInfoCollector(temp_project)
        description = collector.collect_project_description()

        assert description is not None and "JavaScript package description" in description
