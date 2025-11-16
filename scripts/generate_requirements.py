#!/usr/bin/env python3
"""
requirements-*.txtファイルをpyproject.tomlから自動生成するスクリプト
"""

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def generate_requirements_file(extras: list[str], output_file: Path, include_base: bool = False) -> None:
    """
    pyproject.tomlからrequirementsファイルを生成

    Args:
        extras: オプショナル依存関係のリスト（例: ['docgen', 'test']）
        output_file: 出力ファイルのパス
        include_base: 基本依存関係を含めるかどうか
    """
    pyproject_path = PROJECT_ROOT / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    dependencies = []

    # 基本依存関係を追加（include_baseがTrueの場合のみ）
    if include_base and "project" in data and "dependencies" in data["project"]:
        dependencies.extend(data["project"]["dependencies"])

    # オプショナル依存関係を追加
    if "project" in data and "optional-dependencies" in data["project"]:
        optional_deps = data["project"]["optional-dependencies"]
        for extra in extras:
            if extra in optional_deps:
                dependencies.extend(optional_deps[extra])

    # 重複を除去（順序を保持）
    seen = set()
    unique_dependencies = []
    for dep in dependencies:
        # パッケージ名を抽出（バージョン指定を除く）
        package_name = dep.split(">=")[0].split("==")[0].split(";")[0].strip()
        if package_name not in seen:
            seen.add(package_name)
            unique_dependencies.append(dep)

    # ファイルに書き込み
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# このファイルはpyproject.tomlから自動生成されます\n")
        f.write(f"# 手動で編集しないでください\n\n")
        for dep in unique_dependencies:
            f.write(f"{dep}\n")


def main():
    """メイン処理"""
    # requirements-docgen.txtを生成（基本依存関係を含む）
    generate_requirements_file(
        ["docgen"],
        PROJECT_ROOT / "requirements-docgen.txt",
        include_base=True
    )
    print("✓ requirements-docgen.txt を生成しました")

    # requirements-test.txtを生成（基本依存関係を含まない）
    generate_requirements_file(
        ["test"],
        PROJECT_ROOT / "requirements-test.txt",
        include_base=False
    )
    print("✓ requirements-test.txt を生成しました")


if __name__ == "__main__":
    main()

