"""
GenericParserのテスト
"""

from pathlib import Path

import pytest

from docgen.generators.parsers.generic_parser import GenericParser


@pytest.mark.unit
class TestGenericParser:
    """GenericParserのテストクラス"""

    def test_parse_file_rust(self, temp_project):
        """Rustファイルを解析できることを確認"""
        code = """/// サンプル関数
fn hello() {
    println!("Hello");
}
"""
        file_path = temp_project / "main.rs"
        file_path.write_text(code, encoding="utf-8")

        parser = GenericParser(temp_project, language="rust")
        apis = parser.parse_file(file_path)

        assert isinstance(apis, list)

    def test_parse_file_java(self, temp_project):
        """Javaファイルを解析できることを確認"""
        code = """/**
 * サンプルクラス
 */
public class Main {
    /**
     * メインメソッド
     */
    public static void main(String[] args) {
    }
}
"""
        file_path = temp_project / "Main.java"
        file_path.write_text(code, encoding="utf-8")

        parser = GenericParser(temp_project, language="java")
        apis = parser.parse_file(file_path)

        assert isinstance(apis, list)
        # クラスが検出される
        main_class = next((api for api in apis if api["name"] == "Main"), None)
        assert main_class is not None

    def test_parse_file_ruby(self, temp_project):
        """Rubyファイルを解析できることを確認"""
        code = """# サンプルクラス
class Sample
  # メソッド
  def hello
    puts "Hello"
  end
end
"""
        file_path = temp_project / "sample.rb"
        file_path.write_text(code, encoding="utf-8")

        parser = GenericParser(temp_project, language="ruby")
        apis = parser.parse_file(file_path)

        assert isinstance(apis, list)

    def test_get_supported_extensions_rust(self):
        """Rustの拡張子が正しいことを確認"""
        parser = GenericParser(Path("/tmp"), language="rust")
        extensions = parser.get_supported_extensions()

        assert ".rs" in extensions

    def test_get_supported_extensions_java(self):
        """Javaの拡張子が正しいことを確認"""
        parser = GenericParser(Path("/tmp"), language="java")
        extensions = parser.get_supported_extensions()

        assert ".java" in extensions

    def test_parse_project(self, temp_project):
        """プロジェクト全体を解析できることを確認"""
        (temp_project / "main.rs").write_text("fn main() {}\n", encoding="utf-8")

        parser = GenericParser(temp_project, language="rust")
        apis = parser.parse_project()

        assert isinstance(apis, list)
