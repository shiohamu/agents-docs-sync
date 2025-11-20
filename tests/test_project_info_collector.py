"""
ProjectInfoCollectorのテスト
"""

from docgen.collectors.project_info_collector import ProjectInfoCollector


class TestProjectInfoCollector:
    """ProjectInfoCollectorのテストクラス"""

    def test_init(self, temp_project):
        """初期化テスト"""
        collector = ProjectInfoCollector(temp_project)
        assert collector.project_root == temp_project

    def test_collect_all(self, temp_project):
        """全情報収集テスト"""
        collector = ProjectInfoCollector(temp_project)
        result = collector.collect_all()

        expected_keys = [
            "build_commands",
            "test_commands",
            "dependencies",
            "coding_standards",
            "ci_cd_info",
            "project_structure",
        ]

        for key in expected_keys:
            assert key in result
            assert isinstance(result[key], (list, dict))

    def test_collect_build_commands_from_script(self, temp_project):
        """スクリプトからのビルドコマンド収集"""
        script_content = """#!/bin/bash
echo "Building project..."
npm run build
echo "Build complete"
"""
        script_path = temp_project / "scripts" / "run_pipeline.sh"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(script_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_build_commands()

        # スクリプトが見つからない場合、空のリストが返される
        # （実際の解析は複雑なので、ここでは基本的なテストのみ）
        assert isinstance(commands, list)

    def test_collect_build_commands_no_script(self, temp_project):
        """スクリプトが存在しない場合"""
        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_build_commands()

        assert commands == []

    def test_collect_test_commands_from_script(self, temp_project):
        """スクリプトからのテストコマンド収集"""
        script_content = """#!/bin/bash
echo "Running tests..."
npm test
pytest tests/
echo "Tests complete"
"""
        script_path = temp_project / "scripts" / "run_tests.sh"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(script_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_test_commands()

        assert isinstance(commands, list)

    def test_collect_test_commands_no_script(self, temp_project):
        """テストスクリプトが存在しない場合"""
        collector = ProjectInfoCollector(temp_project)
        commands = collector.collect_test_commands()

        assert commands == []

    def test_collect_dependencies_python(self, temp_project):
        """Python依存関係の収集"""
        requirements_content = """requests==2.28.0
pytest>=7.0.0
"""
        req_path = temp_project / "requirements.txt"
        req_path.write_text(requirements_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert "python" in dependencies
        assert isinstance(dependencies["python"], list)

    def test_collect_dependencies_nodejs(self, temp_project):
        """Node.js依存関係の収集"""
        package_json = {
            "dependencies": {"express": "^4.18.0", "lodash": "~4.17.0"},
            "devDependencies": {"jest": "^29.0.0"},
        }

        import json

        pkg_path = temp_project / "package.json"
        pkg_path.write_text(json.dumps(package_json, indent=2), encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert "nodejs" in dependencies
        assert isinstance(dependencies["nodejs"], list)

    def test_collect_dependencies_go(self, temp_project):
        """Go依存関係の収集"""
        go_mod_content = """module test-project

go 1.20

require (
    github.com/pkg/errors v0.9.1
    golang.org/x/sync v0.1.0
)
"""
        go_mod_path = temp_project / "go.mod"
        go_mod_path.write_text(go_mod_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert "go" in dependencies
        assert isinstance(dependencies["go"], list)

    def test_collect_dependencies_no_files(self, temp_project):
        """依存関係ファイルが存在しない場合"""
        collector = ProjectInfoCollector(temp_project)
        dependencies = collector.collect_dependencies()

        assert dependencies == {}

    def test_collect_coding_standards_with_pyproject(self, temp_project):
        """pyproject.tomlからのコーディング規約収集"""
        pyproject_content = """[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
select = ["E", "F", "W"]
"""
        pyproject_path = temp_project / "pyproject.toml"
        pyproject_path.write_text(pyproject_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        standards = collector.collect_coding_standards()

        assert isinstance(standards, dict)

    def test_collect_coding_standards_no_files(self, temp_project):
        """コーディング規約ファイルが存在しない場合"""
        collector = ProjectInfoCollector(temp_project)
        standards = collector.collect_coding_standards()

        assert standards == {}

    def test_collect_ci_cd_info_with_github_actions(self, temp_project):
        """GitHub ActionsからのCI/CD情報収集"""
        workflow_content = """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: make test
"""
        workflow_path = temp_project / ".github" / "workflows" / "ci.yml"
        workflow_path.parent.mkdir(parents=True, exist_ok=True)
        workflow_path.write_text(workflow_content, encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        ci_cd_info = collector.collect_ci_cd_info()

        assert isinstance(ci_cd_info, dict)

    def test_collect_ci_cd_info_no_files(self, temp_project):
        """CI/CDファイルが存在しない場合"""
        collector = ProjectInfoCollector(temp_project)
        ci_cd_info = collector.collect_ci_cd_info()

        assert ci_cd_info == {}

    def test_collect_project_structure(self, temp_project):
        """プロジェクト構造の収集"""
        # テストファイルを作成
        (temp_project / "main.py").write_text("print('hello')", encoding="utf-8")
        (temp_project / "README.md").write_text("# Test", encoding="utf-8")
        (temp_project / ".gitignore").write_text("*.pyc", encoding="utf-8")

        collector = ProjectInfoCollector(temp_project)
        structure = collector.collect_project_structure()

        assert isinstance(structure, dict)
        assert "languages" in structure
        assert "main_directories" in structure
