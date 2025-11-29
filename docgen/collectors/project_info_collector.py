"""
プロジェクト情報収集モジュール
ビルド/テスト手順、コーディング規約、依存関係などの情報を収集
"""

import json
from pathlib import Path
import re
from typing import Any

from ..models.project import ProjectInfo
from ..utils.logger import get_logger
from .collector_utils import BuildCommandCollector


class ProjectInfoCollector:
    """プロジェクト情報収集クラス

    プロジェクトのビルド/テスト手順、依存関係、コーディング規約などを収集する。
    """

    # ファイルパス定数
    # スクリプトディレクトリ
    SCRIPTS_DIR = "scripts"
    RUN_PIPELINE_SCRIPT = "run_pipeline.sh"
    RUN_TESTS_SCRIPT = "run_tests.sh"
    MAKEFILE_NAMES = ["Makefile", "makefile"]
    REQUIREMENTS_FILES = ["requirements.txt", "requirements-docgen.txt", "requirements-test.txt"]
    PACKAGE_JSON = "package.json"
    PYPROJECT_TOML = "pyproject.toml"
    PYTEST_INI = "pytest.ini"
    GO_MOD = "go.mod"
    CARGO_TOML = "Cargo.toml"
    SETUP_PY = "setup.py"
    EDITORCONFIG = ".editorconfig"
    PRETTIER_FILES = [".prettierrc", "prettier.config.js", ".prettierrc.json"]
    GITHUB_WORKFLOWS_DIR = ".github/workflows"
    MAIN_PY = "main.py"
    INIT_PY = "__init__.py"
    README_FILES = ["README.md", "README.rst"]
    CHANGELOG = "CHANGELOG.md"
    LICENSE = "LICENSE"

    def __init__(
        self,
        project_root: Path,
        package_managers: dict[str, str] | None = None,
        logger: Any | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            package_managers: 言語ごとのパッケージマネージャ辞書
            logger: ロガーインスタンス
        """
        self.project_root: Path = project_root
        self.package_managers = package_managers or {}
        self.logger = logger or get_logger(__name__)

        # Initialize sub-collectors
        from .coding_standards_collector import CodingStandardsCollector
        from .dependency_collector import DependencyCollector
        from .structure_analyzer import StructureAnalyzer
        from .test_command_collector import TestCommandCollector

        self.build_collector = BuildCommandCollector(project_root, package_managers)
        self.dependency_collector = DependencyCollector(project_root, logger=self.logger)
        self.test_command_collector = TestCommandCollector(
            project_root, package_managers, logger=self.logger
        )
        self.coding_standards_collector = CodingStandardsCollector(project_root, logger=self.logger)
        self.structure_analyzer = StructureAnalyzer(project_root, logger=self.logger)

    def collect_all(self) -> ProjectInfo:
        """
        すべてのプロジェクト情報を収集

        Returns:
            プロジェクト情報の辞書
        """
        self.logger.info("Collecting project information...")

        # 各情報を収集
        dependencies = self.collect_dependencies()
        test_commands = self.collect_test_commands()
        build_commands = self.build_collector.collect_build_commands()
        coding_standards = self.collect_coding_standards()
        project_structure = self.collect_project_structure()
        project_description = self.collect_project_description()
        key_features = self.collect_key_features()
        ci_cd_info = self.collect_ci_cd_info()

        return ProjectInfo(
            dependencies=dependencies,
            test_commands=test_commands,
            build_commands=build_commands,
            coding_standards=coding_standards,
            project_structure=project_structure,
            description=project_description,
            key_features=key_features,
            ci_cd_info=ci_cd_info,
        )

    def collect_key_features(self) -> list[str]:
        """
        主要機能を収集（プレースホルダー）

        Returns:
            主要機能のリスト
        """
        # TODO: 実装
        return []

    def collect_test_commands(self) -> list[str]:
        """
        テストコマンドを収集

        Returns:
            テストコマンドのリスト
        """
        return self.test_command_collector.collect_test_commands()

    def collect_dependencies(self) -> dict[str, list[str]]:
        """
        依存関係を収集

        Returns:
            依存関係の辞書（言語ごと）
        """
        return self.dependency_collector.collect_dependencies()

    def collect_coding_standards(self) -> dict[str, str | dict[str, Any] | bool]:
        """
        コーディング規約を収集

        Returns:
            コーディング規約の辞書
        """
        return self.coding_standards_collector.collect_coding_standards()

    def collect_ci_cd_info(self) -> dict[str, Any]:
        """
        CI/CD情報を収集

        Returns:
            CI/CD情報の辞書
        """
        ci_cd_info = {}

        # GitHub Actions
        github_workflows = self.project_root / self.GITHUB_WORKFLOWS_DIR
        if github_workflows.exists() and github_workflows.is_dir():
            workflows = []
            for item in github_workflows.iterdir():
                if item.suffix in [".yml", ".yaml"]:
                    workflows.append(item.name)
            if workflows:
                ci_cd_info["github_actions"] = workflows

        return ci_cd_info

    def collect_project_structure(self) -> dict[str, Any]:
        """
        プロジェクト構造を収集

        StructureAnalyzerに委譲して詳細な構造分析を実行

        Returns:
            プロジェクト構造の辞書
        """
        return self.structure_analyzer.analyze()

    def collect_project_description(self) -> str | None:
        """
        プロジェクトの説明を収集

        Returns:
            プロジェクトの説明文（見つからない場合はNone）
        """
        # 1. READMEから説明を取得
        for readme_file in self.README_FILES:
            readme_path = self.project_root / readme_file
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    # 最初の段落を取得（簡易的）
                    lines = content.split("\n")
                    for line in lines:
                        if line.strip() and not line.startswith("#"):
                            return line.strip()
                except Exception:
                    pass

        # 2. pyproject.tomlから説明を取得
        pyproject = self.project_root / self.PYPROJECT_TOML
        if pyproject.exists():
            try:
                import tomllib

                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                if "project" in data and "description" in data["project"]:
                    return data["project"]["description"]
                if (
                    "tool" in data
                    and "poetry" in data["tool"]
                    and "description" in data["tool"]["poetry"]
                ):
                    return data["tool"]["poetry"]["description"]
            except Exception:
                # 簡易パース
                try:
                    content = pyproject.read_text(encoding="utf-8")
                    desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                    if desc_match:
                        return desc_match.group(1)
                except Exception:
                    pass

        # 3. setup.pyから説明を取得
        setup_py = self.project_root / self.SETUP_PY
        if setup_py.exists():
            try:
                content = setup_py.read_text(encoding="utf-8")
                desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    return desc_match.group(1)
            except Exception:
                pass

        # 4. package.jsonから説明を取得
        package_json = self.project_root / self.PACKAGE_JSON
        if package_json.exists():
            try:
                with open(package_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if "description" in data:
                        return data["description"]
            except Exception:
                pass

        return None
