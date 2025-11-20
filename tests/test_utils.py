"""
テストユーティリティ関数
"""

import json
from pathlib import Path
from typing import Any

import yaml


def create_sample_python_file(project_root: Path, filename: str = "sample.py") -> Path:
    """
    サンプルPythonファイルを作成

    Args:
        project_root: プロジェクトルート
        filename: ファイル名

    Returns:
        Path: 作成されたファイルのパス
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

def _private_function():
    """プライベート関数"""
    return "private"
'''
    file_path = project_root / filename
    file_path.write_text(code, encoding="utf-8")
    return file_path


def create_sample_javascript_file(project_root: Path, filename: str = "sample.js") -> Path:
    """
    サンプルJavaScriptファイルを作成

    Args:
        project_root: プロジェクトルート
        filename: ファイル名

    Returns:
        Path: 作成されたファイルのパス
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

// プライベート関数
function _privateFunction() {
    return "private";
}
"""
    file_path = project_root / filename
    file_path.write_text(code, encoding="utf-8")
    return file_path


def create_python_project_structure(project_root: Path) -> None:
    """
    Pythonプロジェクトの基本構造を作成

    Args:
        project_root: プロジェクトルート
    """
    # requirements.txt
    (project_root / "requirements.txt").write_text(
        "pytest>=7.0.0\nrequests>=2.28.0\n", encoding="utf-8"
    )

    # setup.py
    setup_content = """from setuptools import setup, find_packages

setup(
    name="test-project",
    version="1.0.0",
    packages=find_packages(),
)
"""
    (project_root / "setup.py").write_text(setup_content, encoding="utf-8")

    # pyproject.toml
    pyproject_content = """[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
"""
    (project_root / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    # サンプルファイル
    create_sample_python_file(project_root, "main.py")


def create_javascript_project_structure(project_root: Path) -> None:
    """
    JavaScriptプロジェクトの基本構造を作成

    Args:
        project_root: プロジェクトルート
    """
    # package.json
    package_json = {
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {"express": "^4.18.0", "lodash": "^4.17.0"},
        "devDependencies": {"jest": "^29.0.0"},
    }
    (project_root / "package.json").write_text(json.dumps(package_json, indent=2), encoding="utf-8")

    # サンプルファイル
    create_sample_javascript_file(project_root, "index.js")


def create_go_project_structure(project_root: Path) -> None:
    """
    Goプロジェクトの基本構造を作成

    Args:
        project_root: プロジェクトルート
    """
    # go.mod
    go_mod_content = """module test-project

go 1.20

require (
    github.com/pkg/errors v0.9.1
    golang.org/x/sync v0.1.0
)
"""
    (project_root / "go.mod").write_text(go_mod_content, encoding="utf-8")

    # サンプルファイル
    go_code = """package main

import (
    "fmt"
    "github.com/pkg/errors"
)

// HelloWorld は挨拶を返す関数
func HelloWorld(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

// SampleStruct はサンプル構造体
type SampleStruct struct {
    Value int
}

// NewSampleStruct はコンストラクタ
func NewSampleStruct(value int) *SampleStruct {
    return &SampleStruct{Value: value}
}

// GetValue は値を取得
func (s *SampleStruct) GetValue() int {
    return s.Value
}

func main() {
    fmt.Println(HelloWorld("World"))
}
"""
    (project_root / "main.go").write_text(go_code, encoding="utf-8")


def create_config_file(
    project_root: Path, config: dict[str, Any], filename: str = "config.yaml"
) -> Path:
    """
    設定ファイルを作成

    Args:
        project_root: プロジェクトルート
        config: 設定内容
        filename: ファイル名

    Returns:
        Path: 作成されたファイルのパス
    """
    config_dir = project_root / ".docgen"
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / filename

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    return config_path


def assert_file_exists_and_not_empty(file_path: Path) -> None:
    """
    ファイルが存在し、空でないことを確認

    Args:
        file_path: 確認するファイルのパス
    """
    assert file_path.exists(), f"ファイルが存在しません: {file_path}"
    content = file_path.read_text(encoding="utf-8")
    assert len(content.strip()) > 0, f"ファイルが空です: {file_path}"


def assert_file_contains_text(file_path: Path, *texts: str) -> None:
    """
    ファイルが指定されたテキストを含むことを確認

    Args:
        file_path: 確認するファイルのパス
        texts: 含まれるべきテキスト
    """
    content = file_path.read_text(encoding="utf-8")
    for text in texts:
        assert text in content, f"ファイルにテキストが見つかりません: {text}"


def assert_file_not_contains_text(file_path: Path, *texts: str) -> None:
    """
    ファイルが指定されたテキストを含まないことを確認

    Args:
        file_path: 確認するファイルのパス
        texts: 含まれないべきテキスト
    """
    content = file_path.read_text(encoding="utf-8")
    for text in texts:
        assert text not in content, f"ファイルに予期しないテキストが見つかりました: {text}"


def create_test_data_factory():
    """
    テストデータ作成のファクトリ関数を返す

    Returns:
        dict: 言語ごとのデータ作成関数
    """
    return {
        "python": create_python_project_structure,
        "javascript": create_javascript_project_structure,
        "go": create_go_project_structure,
    }
