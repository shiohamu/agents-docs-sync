"""
uv関連のユーティリティ関数
"""

from pathlib import Path


def detect_uv_usage(project_root: Path) -> bool:
    """
    プロジェクトがuvを使用しているかを検出

    Args:
        project_root: プロジェクトのルートディレクトリ

    Returns:
        uvを使用している場合True
    """
    # uv.lockファイルが存在する場合
    if (project_root / "uv.lock").exists():
        return True

    # pyproject.tomlに[tool.uv]セクションがある場合
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        return _has_uv_config(pyproject)

    return False


def _has_uv_config(pyproject_path: Path) -> bool:
    """pyproject.tomlにuv設定があるかを確認"""
    try:
        import tomllib

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return "tool" in data and "uv" in data["tool"]
    except ImportError:
        # tomllibが利用できない場合、テキスト検索で確認
        try:
            with open(pyproject_path, encoding="utf-8") as f:
                content = f.read()
                return "[tool.uv]" in content
        except Exception:
            return False
    except Exception:
        return False


def wrap_command_with_uv(command: str) -> str:
    """
    uvを使用する場合のコマンドをuv runでラップ

    Args:
        command: 元のコマンド

    Returns:
        uv runでラップされたコマンド
    """
    # すでにuvで始まっている場合はそのまま
    if command.startswith("uv"):
        return command

    # python/pytestなどのコマンドをuv runでラップ
    if command.startswith(("python", "pytest")):
        return f"uv run {command}"

    # その他のコマンドはuv runでラップ
    return f"uv run {command}"
