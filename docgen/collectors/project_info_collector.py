"""
プロジェクト情報収集モジュール
ビルド/テスト手順、コーディング規約、依存関係などの情報を収集
"""

import json
from pathlib import Path
import re
from typing import Any

from ..models import ProjectInfo


class ProjectInfoCollector:
    """プロジェクト情報収集クラス"""

    def __init__(self, project_root: Path, package_managers: dict[str, str] | None = None):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            package_managers: 言語ごとのパッケージマネージャ辞書
        """
        self.project_root: Path = project_root
        self.package_managers = package_managers or {}

    def collect_all(self) -> ProjectInfo:
        """
        すべてのプロジェクト情報を収集

        Returns:
            プロジェクト情報の辞書
        """
        return ProjectInfo(
            description=self.collect_project_description(),
            build_commands=self.collect_build_commands(),
            test_commands=self.collect_test_commands(),
            dependencies=self.collect_dependencies(),
            coding_standards=self.collect_coding_standards(),
            ci_cd_info=self.collect_ci_cd_info(),
            project_structure=self.collect_project_structure(),
        )

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
                    or line.strip().startswith("go")
                ):
                    command = line.strip()
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if command.startswith("python"):
                            command = f"uv run {command}"
                    commands.append(command)

        # Makefile から収集
        makefile = self.project_root / "Makefile"
        if makefile.exists():
            content = makefile.read_text(encoding="utf-8")
            # タブで始まるコマンド行を抽出
            for line in content.split("\n"):
                if line.startswith("\t") and line.strip():
                    # \tを削除してコマンドを追加
                    command = line.lstrip("\t")
                    if command and not command.startswith("@"):
                        # uvプロジェクトの場合はpythonコマンドにuv runをつける
                        if (
                            "python" in self.package_managers
                            and self.package_managers["python"] == "uv"
                        ):
                            if command.startswith("python") or command.startswith("pytest"):
                                command = f"uv run {command}"
                        commands.append(command)

        # package.json から収集
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data:
                        pm = self.package_managers.get("javascript", "npm")
                        for script_name, script_cmd in data["scripts"].items():
                            if pm == "pnpm":
                                commands.append(f"pnpm run {script_name}")
                            elif pm == "yarn":
                                commands.append(f"yarn run {script_name}")
                            else:  # npm
                                commands.append(f"npm run {script_name}")
            except (json.JSONDecodeError, KeyError):
                pass

        # Goプロジェクトの場合
        if "go" in self.package_managers:
            pm = self.package_managers["go"]
            if pm == "go":
                commands.append("go build")
            elif pm == "dep":
                commands.append("dep ensure")
            elif pm == "glide":
                commands.append("glide install")

        # 重複を順序を保って排除
        seen = set()
        unique_commands = []
        for c in commands:
            if c not in seen:
                unique_commands.append(c)
                seen.add(c)
        return unique_commands

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
                        command = match.group(0)
                        # uvプロジェクトの場合はpythonコマンドにuv runをつける
                        if (
                            "python" in self.package_managers
                            and self.package_managers["python"] == "uv"
                        ):
                            if command.startswith("python") or command.startswith("pytest"):
                                command = f"uv run {command}"
                        commands.append(command)

        # Makefile から収集
        makefile = self.project_root / "Makefile"
        if makefile.exists():
            content = makefile.read_text(encoding="utf-8")
            # testターゲットのコマンド行を抽出
            in_test_target = False
            for line in content.split("\n"):
                if line.strip() == "test:":
                    in_test_target = True
                elif line.strip().endswith(":") and in_test_target:
                    break  # 次のターゲット
                elif in_test_target and line.startswith("\t") and line.strip():
                    command = line.lstrip("\t")
                    if command and not command.startswith("@"):
                        # uvプロジェクトの場合はpythonコマンドにuv runをつける
                        if (
                            "python" in self.package_managers
                            and self.package_managers["python"] == "uv"
                        ):
                            if command.startswith("python") or command.startswith("pytest"):
                                command = f"uv run {command}"
                        commands.append(command)

        # Pythonプロジェクトの場合
        if "python" in self.package_managers:
            pm = self.package_managers["python"]
            if pm == "uv":
                commands.append("uv run pytest tests/ -v --tb=short")
            elif pm == "poetry":
                commands.append("poetry run pytest tests/ -v --tb=short")
            else:  # pip
                commands.append("pytest tests/ -v --tb=short")
        # pytest.ini から収集（パッケージマネージャが指定されていない場合）
        elif (self.project_root / "pytest.ini").exists():
            command = "pytest tests/ -v --tb=short"
            # uvプロジェクトの場合はuv runをつける
            if "python" in self.package_managers and self.package_managers["python"] == "uv":
                command = f"uv run {command}"
            commands.append(command)

        # package.json から収集
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "scripts" in data and "test" in data["scripts"]:
                        pm = self.package_managers.get("javascript", "npm")
                        if pm == "pnpm":
                            commands.append("pnpm test")
                        elif pm == "yarn":
                            commands.append("yarn test")
                        else:  # npm
                            commands.append("npm test")
            except (json.JSONDecodeError, KeyError):
                pass

        # Goプロジェクトの場合
        if "go" in self.package_managers:
            pm = self.package_managers["go"]
            if pm == "go":
                commands.append("go test ./...")

        # 重複を順序を保って排除
        seen = set()
        unique_commands = []
        for c in commands:
            if c not in seen:
                unique_commands.append(c)
                seen.add(c)
        return unique_commands

    def collect_dependencies(self) -> dict[str, list[str]]:
        """
        依存関係を収集

        Returns:
            依存関係の辞書（言語ごと）
        """
        dependencies = {}

        # Python依存関係
        python_deps = []
        for req_file in [
            "requirements.txt",
            "requirements-docgen.txt",
            "requirements-test.txt",
        ]:
            req_path = self.project_root / req_file
            if req_path.exists():
                with open(req_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            python_deps.append(line)
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

        # Go依存関係
        go_mod = self.project_root / "go.mod"
        if go_mod.exists():
            go_deps = []
            try:
                content = go_mod.read_text(encoding="utf-8")
                lines = content.split("\n")
                in_require = False
                for line in lines:
                    line = line.strip()
                    if line.startswith("require ("):
                        in_require = True
                        continue
                    if in_require and line == ")":
                        in_require = False
                        continue
                    if in_require or line.startswith("require "):
                        if in_require:
                            parts = line.split()
                            if parts:
                                go_deps.append(parts[0])
                        else:
                            parts = line.split()
                            if len(parts) >= 2:
                                go_deps.append(parts[1])
                if go_deps:
                    dependencies["go"] = go_deps
            except Exception:
                pass

        # 重複を順序を保って排除（各依存関係リストごとに適用）
        def _dedup_preserve_order(items: list[str]) -> list[str]:
            seen_local = set()
            out = []
            for it in items:
                if it not in seen_local:
                    out.append(it)
                    seen_local.add(it)
            return out

        if "python" in dependencies:
            dependencies["python"] = _dedup_preserve_order(dependencies["python"])
        if "nodejs" in dependencies:
            dependencies["nodejs"] = _dedup_preserve_order(dependencies["nodejs"])
        if "go" in dependencies:
            dependencies["go"] = _dedup_preserve_order(dependencies["go"])

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
                    except ImportError:
                        # tomliがインストールされていない場合、簡易的な解析にフォールバック
                        raise ImportError("tomli not available") from None

                if "tool" in data:
                    tools = data["tool"]
                    if "black" in tools:
                        standards["formatter"] = "black"
                        standards["black_config"] = tools["black"]
                    if "isort" in tools:
                        standards["import_sorter"] = "isort"
                        standards["isort_config"] = tools["isort"]
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
            "important_files": [],
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
                structure["main_directories"].append(item.name + "/")
            elif item.is_file() and item.name in [
                "README.md",
                "README.rst",
                "CHANGELOG.md",
                "LICENSE",
            ]:
                structure["important_files"].append(item.name)

        return structure

    def collect_project_description(self) -> str | None:
        """
        プロジェクトの説明を収集

        Returns:
            プロジェクトの説明文（見つからない場合はNone）
        """
        # 1. pyproject.tomlのdescriptionから取得（優先）
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            try:
                import sys

                if sys.version_info >= (3, 11):
                    import tomllib

                    with open(pyproject, "rb") as f:
                        data = tomllib.load(f)
                else:
                    try:
                        import tomli

                        with open(pyproject, "rb") as f:
                            data = tomli.load(f)
                    except ImportError:
                        data = {}

                if "project" in data and "description" in data["project"]:
                    description = data["project"]["description"]
                    if description and len(description) > 10:
                        return description
            except Exception:
                pass

        # 2. README.mdから説明を取得
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            # 最初の段落を抽出（# タイトルの後の最初の非空行）
            lines = readme_content.split("\n")
            found_title = False
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    found_title = True
                    continue
                if found_title and line and not line.startswith("<!--"):
                    # 汎用的なテンプレート文をスキップ
                    if "このプロジェクトの説明をここに記述してください" not in line:
                        return line
                    break

        # 3. setup.pyから説明を取得
        setup_py = self.project_root / "setup.py"
        if setup_py.exists():
            try:
                content = setup_py.read_text(encoding="utf-8")
                # description= または long_description= を探す
                desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    return desc_match.group(1)
                long_desc_match = re.search(r'long_description\s*=\s*["\']([^"\']+)["\']', content)
                if long_desc_match:
                    return long_desc_match.group(1)
            except Exception:
                pass

        # 4. package.jsonから説明を取得
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "description" in data:
                        return data["description"]
            except Exception:
                pass

        # 5. main.pyのdocstringから取得
        main_py = self.project_root / "main.py"
        if main_py.exists():
            try:
                content = main_py.read_text(encoding="utf-8")
                # モジュールレベルのdocstringを抽出
                # """...""" または '''...''' のパターンを探す
                docstring_pattern = r'"""(.*?)"""'
                match = re.search(docstring_pattern, content, re.DOTALL)
                if match:
                    docstring = match.group(1).strip()
                    if docstring and len(docstring) > 10:  # 短すぎる場合はスキップ
                        return docstring.split("\n")[0]  # 最初の行のみ
            except Exception:
                pass

        # 6. __init__.pyのdocstringから取得
        init_py = self.project_root / "__init__.py"
        if init_py.exists():
            try:
                content = init_py.read_text(encoding="utf-8")
                docstring_pattern = r'"""(.*?)"""'
                match = re.search(docstring_pattern, content, re.DOTALL)
                if match:
                    docstring = match.group(1).strip()
                    if docstring and len(docstring) > 10:
                        return docstring.split("\n")[0]
            except Exception:
                pass

        return None
