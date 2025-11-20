"""
プロジェクト情報収集モジュール
ビルド/テスト手順、コーディング規約、依存関係などの情報を収集
"""

import json
from pathlib import Path
import re
from typing import Any


class ProjectInfoCollector:
    """プロジェクト情報収集クラス"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root

    def collect_all(self) -> dict[str, Any]:
        """
        すべてのプロジェクト情報を収集

        Returns:
            プロジェクト情報の辞書
        """
        return {
            "build_commands": self.collect_build_commands(),
            "test_commands": self.collect_test_commands(),
            "dependencies": self.collect_dependencies(),
            "coding_standards": self.collect_coding_standards(),
            "ci_cd_info": self.collect_ci_cd_info(),
            "project_structure": self.collect_project_structure(),
        }

    def collect_build_commands(self) -> list[str]:
        """
        ビルドコマンドを収集

        Returns:
            ビルドコマンドのリスト
        """
        commands = []

        # scripts/run_pipeline.sh から収集
        pipeline_script = self.project_root / "scripts" / "run_pipeline.sh"
        if pipeline_script.exists():
            content = pipeline_script.read_text(encoding="utf-8")
            # コマンド行を抽出（簡易的な実装）
            for line in content.split("\n"):
                if (
                    line.strip().startswith("python")
                    or line.strip().startswith("npm")
                    or line.strip().startswith("make")
                ):
                    commands.append(line.strip())

        # Makefile から収集
        makefile = self.project_root / "Makefile"
        if makefile.exists():
            content = makefile.read_text(encoding="utf-8")
            # .PHONY やターゲットを抽出
            for line in content.split("\n"):
                if re.match(r"^\w+:", line) and not line.startswith(".PHONY"):
                    target = line.split(":")[0].strip()
                    commands.append(f"make {target}")

        # package.json から収集
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data:
                        for script_name, script_cmd in data["scripts"].items():
                            commands.append(f"npm run {script_name}")
            except (json.JSONDecodeError, KeyError):
                pass

        # uv.lock がある場合、uv sync を追加
        uv_lock = self.project_root / "uv.lock"
        if uv_lock.exists() and "uv sync" not in commands:
            commands.insert(0, "uv sync")  # 最初に実行する

        return commands

    def collect_test_commands(self) -> list[str]:
        """
        テストコマンドを収集

        Returns:
            テストコマンドのリスト
        """
        commands = []

        # scripts/run_tests.sh から収集
        test_script = self.project_root / "scripts" / "run_tests.sh"
        if test_script.exists():
            content = test_script.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if "pytest" in line or "test" in line.lower():
                    # コマンド行を抽出
                    match = re.search(r"(pytest|python.*test|npm.*test|make.*test)", line)
                    if match:
                        commands.append(match.group(0))

        # pytest.ini から収集
        pytest_ini = self.project_root / "pytest.ini"
        if pytest_ini.exists():
            commands.append("pytest tests/ -v --tb=short")

        # package.json の test スクリプトから収集
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data and "test" in data["scripts"]:
                        commands.append("npm test")
            except (json.JSONDecodeError, KeyError):
                pass

        # uvを使用している場合、uv run pytest を追加
        uv_lock = self.project_root / "uv.lock"
        if uv_lock.exists() and not any("pytest" in cmd for cmd in commands):
            commands.append("uv run pytest tests/ -v --tb=short")

        return list(set(commands))  # 重複を除去

    def collect_dependencies(self) -> dict[str, list[str]]:
        """
        依存関係を収集

        Returns:
            依存関係の辞書（言語ごと）
        """
        dependencies = {}

        # Python依存関係
        python_deps = []
        for req_file in ["requirements.txt", "requirements-docgen.txt", "requirements-test.txt"]:
            req_path = self.project_root / req_file
            if req_path.exists():
                with open(req_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            python_deps.append(line)

        # uv.lock からの依存関係収集
        uv_lock = self.project_root / "uv.lock"
        if uv_lock.exists():
            try:
                import tomllib

                with open(uv_lock, "rb") as f:
                    data = tomllib.load(f)
                    for package in data.get("package", []):
                        if "name" in package and "version" in package:
                            dep_str = f"{package['name']}=={package['version']}"
                            if dep_str not in python_deps:
                                python_deps.append(dep_str)
            except ImportError:
                # tomllibが利用できない場合、簡易的な解析にフォールバック
                try:
                    with open(uv_lock, encoding="utf-8") as f:
                        content = f.read()
                        # name = "package_name" のパターンを検索
                        name_pattern = r'name = "([^"]+)"'
                        version_pattern = r'version = "([^"]+)"'
                        names = re.findall(name_pattern, content)
                        versions = re.findall(version_pattern, content)
                        for name, version in zip(names, versions):
                            if name != "agents-docs-sync":  # プロジェクト自身を除外
                                dep_str = f"{name}=={version}"
                                if dep_str not in python_deps:
                                    python_deps.append(dep_str)
                except Exception:
                    pass

        if python_deps:
            dependencies["python"] = python_deps

        # Node.js依存関係
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "dependencies" in data:
                        node_deps = [
                            f"{name}@{version}" for name, version in data["dependencies"].items()
                        ]
                        dependencies["nodejs"] = node_deps
            except (json.JSONDecodeError, KeyError):
                pass

        return dependencies

    def collect_coding_standards(self) -> dict[str, Any]:
        """
        コーディング規約を収集

        Returns:
            コーディング規約の辞書
        """
        standards = {}

        # pyproject.toml から収集
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            try:
                # Python 3.11以降では標準ライブラリのtomllibを使用
                import sys

                if sys.version_info >= (3, 11):
                    import tomllib

                    with open(pyproject, "rb") as f:
                        data = tomllib.load(f)
                else:
                    # Python 3.10以前ではtomliを使用（オプショナル）
                    try:
                        import tomli

                        with open(pyproject, "rb") as f:
                            data = tomli.load(f)
                    except ImportError as err:
                        # tomliがインストールされていない場合、簡易的な解析にフォールバック
                        raise ImportError("tomli not available") from err

                if "tool" in data:
                    tools = data["tool"]
                    if "black" in tools:
                        standards["formatter"] = "black"
                        standards["black_config"] = tools["black"]
                    if "ruff" in tools:
                        standards["linter"] = "ruff"
                        standards["ruff_config"] = tools["ruff"]
            except (ImportError, Exception):
                # TOML解析が失敗した場合、簡易的な解析にフォールバック
                content = pyproject.read_text(encoding="utf-8")
                if "black" in content:
                    standards["formatter"] = "black"
                if "ruff" in content:
                    standards["linter"] = "ruff"

        # .editorconfig から収集
        editorconfig = self.project_root / ".editorconfig"
        if editorconfig.exists():
            standards["editorconfig"] = True

        # prettier.config.js または .prettierrc から収集
        for prettier_file in [".prettierrc", "prettier.config.js", ".prettierrc.json"]:
            prettier_path = self.project_root / prettier_file
            if prettier_path.exists():
                standards["formatter"] = "prettier"
                break

        return standards

    def collect_ci_cd_info(self) -> dict[str, Any]:
        """
        CI/CD情報を収集

        Returns:
            CI/CD情報の辞書
        """
        ci_info = {}

        # GitHub Actions
        workflows_dir = self.project_root / ".github" / "workflows"
        if workflows_dir.exists():
            workflows = []
            for workflow_file in workflows_dir.glob("*.yml"):
                workflows.append(workflow_file.name)
            if workflows:
                ci_info["github_actions"] = workflows

        return ci_info

    def collect_project_structure(self) -> dict[str, Any]:
        """
        プロジェクト構造を収集

        Returns:
            プロジェクト構造の辞書
        """
        structure = {
            "languages": [],
            "main_directories": [],
        }

        # 言語の検出（簡易版）
        if (self.project_root / "requirements.txt").exists() or (
            self.project_root / "pyproject.toml"
        ).exists():
            structure["languages"].append("python")
        if (self.project_root / "package.json").exists():
            structure["languages"].append("javascript")
        if (self.project_root / "go.mod").exists():
            structure["languages"].append("go")

        # 主要ディレクトリ
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                structure["main_directories"].append(item.name)

        return structure
