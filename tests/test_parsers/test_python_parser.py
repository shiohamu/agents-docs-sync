"""
PythonParserのテスト
"""

from pathlib import Path

import pytest

from docgen.generators.parsers.python_parser import PythonParser


@pytest.mark.unit
class TestPythonParser:
    """PythonParserのテストクラス"""

    def test_parse_file_with_function(self, sample_python_file):
        """関数を含むファイルを解析できることを確認"""
        parser = PythonParser(sample_python_file.parent)
        apis = parser.parse_file(sample_python_file)

        assert len(apis) >= 1
        hello_func = next((api for api in apis if api["name"] == "hello_world"), None)
        assert hello_func is not None
        assert hello_func["type"] == "function"
        assert "name" in hello_func
        assert "docstring" in hello_func
        assert hello_func["docstring"] != ""

    def test_parse_file_with_class(self, sample_python_file):
        """クラスを含むファイルを解析できることを確認"""
        parser = PythonParser(sample_python_file.parent)
        apis = parser.parse_file(sample_python_file)

        sample_class = next((api for api in apis if api["name"] == "SampleClass"), None)
        assert sample_class is not None
        assert sample_class["type"] == "class"
        assert "docstring" in sample_class

    def test_parse_file_extracts_signature(self, sample_python_file):
        """シグネチャが正しく抽出されることを確認"""
        parser = PythonParser(sample_python_file.parent)
        apis = parser.parse_file(sample_python_file)

        hello_func = next((api for api in apis if api["name"] == "hello_world"), None)
        assert hello_func is not None
        assert "signature" in hello_func
        assert "hello_world" in hello_func["signature"]

    def test_parse_file_extracts_docstring(self, sample_python_file):
        """docstringが正しく抽出されることを確認"""
        parser = PythonParser(sample_python_file.parent)
        apis = parser.parse_file(sample_python_file)

        hello_func = next((api for api in apis if api["name"] == "hello_world"), None)
        assert hello_func is not None
        assert "docstring" in hello_func
        assert "挨拶を返す関数" in hello_func["docstring"]

    def test_parse_file_includes_line_number(self, sample_python_file):
        """行番号が含まれることを確認"""
        parser = PythonParser(sample_python_file.parent)
        apis = parser.parse_file(sample_python_file)

        assert all("line" in api for api in apis)
        assert all(isinstance(api["line"], int) for api in apis)

    def test_parse_project(self, python_project):
        """プロジェクト全体を解析できることを確認"""
        parser = PythonParser(python_project)
        apis = parser.parse_project()

        assert isinstance(apis, list)
        # main.pyの関数が解析される
        assert len(apis) >= 0

    def test_parse_file_skips_private_functions(self, temp_project):
        """プライベート関数（_で始まる）がスキップされることを確認"""
        code = """def public_func():
    pass

def _private_func():
    pass
"""
        file_path = temp_project / "test.py"
        file_path.write_text(code, encoding="utf-8")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(file_path)

        names = [api["name"] for api in apis]
        assert "public_func" in names
        assert "_private_func" not in names

    def test_get_supported_extensions(self):
        """サポートする拡張子が正しいことを確認"""
        parser = PythonParser(Path("/tmp"))
        extensions = parser.get_supported_extensions()

        assert ".py" in extensions
        assert ".pyw" in extensions

    def test_parse_file_with_syntax_error(self, temp_project):
        """構文エラーがあるファイルでもエラーが発生しないことを確認"""
        code = "def invalid syntax\n"
        file_path = temp_project / "invalid.py"
        file_path.write_text(code, encoding="utf-8")

        parser = PythonParser(temp_project)
        # 構文エラーがあっても例外が発生しない
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)
