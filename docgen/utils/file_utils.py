"""
ファイル操作ユーティリティ
"""

import json
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    tomllib = None

try:
    import yaml
except ImportError:
    yaml = None


def safe_read_file(file_path: Path, encoding: str = "utf-8") -> str | None:
    """
    ファイルを安全に読み込む

    Args:
        file_path: 読み込むファイルのパス
        encoding: 文字エンコーディング

    Returns:
        ファイルの内容。読み込み失敗時はNone
    """
    try:
        if not file_path.exists():
            return None
        return file_path.read_text(encoding=encoding)
    except (OSError, UnicodeDecodeError):
        return None


def save_yaml_file(file_path: Path, data: dict[str, Any]) -> bool:
    """
    YAMLファイルを保存

    Args:
        file_path: 保存先ファイルパス
        data: 保存するデータ

    Returns:
        成功した場合はTrue
    """
    if yaml is None:
        return False
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception:
        return False


def safe_write_file(file_path: Path, content: str, encoding: str = "utf-8") -> bool:
    """
    ファイルを安全に書き込む

    Args:
        file_path: 書き込むファイルのパス
        content: 書き込む内容
        encoding: 文字エンコーディング

    Returns:
        成功した場合はTrue
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return True
    except OSError:
        return False


def safe_read_json(file_path: Path) -> Any | None:
    """
    JSONファイルを安全に読み込む

    Args:
        file_path: JSONファイルのパス

    Returns:
        パースされたJSONデータ。失敗時はNone
    """
    try:
        if not file_path.exists():
            return None
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def load_toml_file(file_path: Path) -> dict[str, Any] | None:
    """
    TOMLファイルを読み込む

    Args:
        file_path: 読み込むTOMLファイルのパス

    Returns:
        読み込んだ辞書。読み込み失敗時はNone
    """
    if tomllib is None:
        return None
    try:
        if not file_path.exists():
            return None
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return None


def find_files_with_extensions(root_dir: Path, extensions: list[str]) -> list[Path]:
    """
    指定された拡張子のファイルを検索

    Args:
        root_dir: 検索するルートディレクトリ
        extensions: 拡張子のリスト（例: ['.py', '.js']）

    Returns:
        見つかったファイルのリスト
    """
    files = []
    for ext in extensions:
        files.extend(root_dir.glob(f"**/*{ext}"))
    return sorted(files)


def safe_read_yaml(file_path: Path) -> Any | None:
    """
    YAMLファイルを安全に読み込む

    Args:
        file_path: YAMLファイルのパス

    Returns:
        パースされたYAMLデータ。失敗時はNone
    """
    if yaml is None:
        return None
    try:
        if not file_path.exists():
            return None
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except (OSError, yaml.YAMLError):
        return None


def safe_read_toml(file_path: Path) -> Any | None:
    """
    TOMLファイルを安全に読み込む

    Args:
        file_path: TOMLファイルのパス

    Returns:
        パースされたTOMLデータ。失敗時はNone
    """
    if tomllib is None:
        return None
    try:
        if not file_path.exists():
            return None
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except OSError:
        return None


def find_files_with_extensions(
    project_root: Path, extensions: list[str], exclude_dirs: list[str] | None = None
) -> list[Path]:
    """
    指定された拡張子のファイルを検索

    Args:
        project_root: プロジェクトルート
        extensions: 拡張子のリスト（例: ['.py', '.js']）
        exclude_dirs: 除外するディレクトリ名のリスト

    Returns:
        見つかったファイルのパスリスト
    """
    if exclude_dirs is None:
        exclude_dirs = [".git", "__pycache__", "node_modules", ".venv", "venv"]

    files = []
    project_root_resolved = project_root.resolve()

    for ext in extensions:
        for file_path in project_root.rglob(f"*{ext}"):
            try:
                # 除外ディレクトリをチェック
                if any(part in exclude_dirs for part in file_path.parts):
                    continue

                # プロジェクトルート外をチェック
                file_path_resolved = file_path.resolve()
                file_path_resolved.relative_to(project_root_resolved)

                # シンボリックリンクをスキップ
                if file_path.is_symlink():
                    continue

                files.append(file_path)
            except (OSError, ValueError):
                continue

    return files
