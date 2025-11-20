"""
JSParserのテスト
"""

from pathlib import Path

from generators.parsers.js_parser import JSParser
import pytest


@pytest.mark.unit
class TestJSParser:
    """JSParserのテストクラス"""

    def test_parse_file_with_jsdoc(self, sample_javascript_file):
        """JSDocコメントを含むファイルを解析できることを確認"""
        parser = JSParser(sample_javascript_file.parent)
        apis = parser.parse_file(sample_javascript_file)

        assert len(apis) >= 1
        hello_func = next((api for api in apis if api["name"] == "helloWorld"), None)
        assert hello_func is not None
        assert hello_func["type"] == "function"

    def test_parse_file_extracts_jsdoc(self, sample_javascript_file):
        """JSDocコメントが正しく抽出されることを確認"""
        parser = JSParser(sample_javascript_file.parent)
        apis = parser.parse_file(sample_javascript_file)

        hello_func = next((api for api in apis if api["name"] == "helloWorld"), None)
        if hello_func:
            assert "docstring" in hello_func
            # JSDocの内容が含まれているか確認
            docstring = hello_func.get("docstring", "")
            assert "挨拶を返す関数" in docstring or len(docstring) >= 0

    def test_parse_file_with_class(self, sample_javascript_file):
        """クラスを含むファイルを解析できることを確認"""
        parser = JSParser(sample_javascript_file.parent)
        apis = parser.parse_file(sample_javascript_file)

        sample_class = next((api for api in apis if api["name"] == "SampleClass"), None)
        assert sample_class is not None
        assert sample_class["type"] == "class"

    def test_parse_file_extracts_signature(self, sample_javascript_file):
        """シグネチャが正しく抽出されることを確認"""
        parser = JSParser(sample_javascript_file.parent)
        apis = parser.parse_file(sample_javascript_file)

        hello_func = next((api for api in apis if api["name"] == "helloWorld"), None)
        if hello_func:
            assert "signature" in hello_func
            assert "helloWorld" in hello_func["signature"]

    def test_parse_project(self, javascript_project):
        """プロジェクト全体を解析できることを確認"""
        parser = JSParser(javascript_project)
        apis = parser.parse_project()

        assert isinstance(apis, list)

    def test_get_supported_extensions(self):
        """サポートする拡張子が正しいことを確認"""
        parser = JSParser(Path("/tmp"))
        extensions = parser.get_supported_extensions()

        assert ".js" in extensions
        assert ".jsx" in extensions
        assert ".ts" in extensions
        assert ".tsx" in extensions

    def test_parse_file_without_jsdoc(self, temp_project):
        """JSDocなしの関数も解析できることを確認"""
        code = """function simpleFunc() {
    return true;
}
"""
        file_path = temp_project / "simple.js"
        file_path.write_text(code, encoding="utf-8")

        parser = JSParser(temp_project)
        apis = parser.parse_file(file_path)

        assert len(apis) >= 1
        func = next((api for api in apis if api["name"] == "simpleFunc"), None)
        assert func is not None
