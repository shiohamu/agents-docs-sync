"""
プロジェクト構造解析ユーティリティ
"""

from pathlib import Path
from typing import Set


def get_project_structure(project_root: Path, max_depth: int = 2, max_items: int = 20) -> list[str]:
    """
    プロジェクト構造を取得（重要なディレクトリとファイルのみ）

    Args:
        project_root: プロジェクトルート
        max_depth: 最大深さ
        max_items: 最大項目数

    Returns:
        構造の行リスト
    """
    structure = []

    # 重要なディレクトリ（表示する）
    important_dirs: Set[str] = {"docgen", ".github", "docs", "scripts", "tests"}

    # 除外するディレクトリ（キャッシュ、仮想環境など）
    exclude_dirs: Set[str] = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
        ".pytest_cache",
        ".mypy_cache",
        "htmlcov",
        ".coverage",
        "dist",
        "build",
    }

    # 重要なルートレベルのファイル
    important_files: Set[str] = {
        "README.md",
        "AGENTS.md",
        "pyproject.toml",
        "pytest.ini",
        "requirements.txt",
        "requirements-docgen.txt",
        "requirements-test.txt",
        "setup.sh",
        "package.json",
        "go.mod",
        "Makefile",
    }

    def _should_include(item: Path, is_root: bool = False) -> bool:
        """アイテムを含めるべきか判定"""
        if item.is_dir():
            # 重要なディレクトリは含める
            if item.name in important_dirs:
                return True
            # 除外ディレクトリは含めない
            if item.name in exclude_dirs:
                return False
            # ルートレベルでは通常のディレクトリも含める
            if is_root and not item.name.startswith("."):
                return True
            return False
        else:
            # 重要なファイルは含める
            if item.name in important_files:
                return True
            # ルートレベルでは設定ファイルも含める
            if is_root and (
                item.name.endswith((".toml", ".ini", ".sh", ".md", ".txt", ".json"))
                or item.name in {"Dockerfile", "docker-compose.yml"}
            ):
                return True
            return False

    def _add_item(path: Path, prefix: str = "", depth: int = 0):
        """アイテムを構造に追加"""
        if len(structure) >= max_items:
            return

        if depth > max_depth:
            return

        item_name = path.name
        if path.is_dir():
            item_name += "/"

        structure.append(f"{prefix}{item_name}")

        if path.is_dir() and depth < max_depth:
            try:
                children = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for child in children:
                    if _should_include(child, is_root=(depth == 0)):
                        _add_item(child, f"{prefix}  ", depth + 1)
            except OSError:
                pass

    # ルートレベルのアイテムを追加
    try:
        root_items = sorted(project_root.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in root_items:
            if _should_include(item, is_root=True):
                _add_item(item)
    except OSError:
        pass

    return structure
