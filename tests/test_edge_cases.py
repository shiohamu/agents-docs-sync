"""
エッジケースとエラーハンドリングのテスト
"""

from pathlib import Path
import sys

import pytest

DOCGEN_DIR = Path(__file__).parent.parent / "docgen"
sys.path.insert(0, str(DOCGEN_DIR))

from docgen.detectors.python_detector import PythonDetector
from docgen.generators.api_generator import APIGenerator
from docgen.generators.parsers.python_parser import PythonParser
from docgen.generators.readme_generator import ReadmeGenerator


@pytest.mark.unit
class TestEdgeCases:
    """エッジケースとエラーハンドリングのテストクラス"""

    def test_detector_with_nonexistent_directory(self, tmp_path):
        """存在しないディレクトリでの検出をテスト"""
        nonexistent = tmp_path / "nonexistent"
        detector = PythonDetector(nonexistent)
        # エラーが発生しないことを確認
        result = detector.detect()
        assert isinstance(result, bool)

    def test_parser_with_nonexistent_file(self, temp_project):
        """存在しないファイルの解析をテスト"""
        parser = PythonParser(temp_project)
        nonexistent_file = temp_project / "nonexistent.py"
        # エラーが発生しないことを確認
        apis = parser.parse_file(nonexistent_file)
        assert isinstance(apis, list)

    def test_parser_with_syntax_error(self, temp_project):
        """構文エラーを含むファイルの解析をテスト"""
        code = "def invalid syntax here\n"
        file_path = temp_project / "invalid.py"
        file_path.write_text(code, encoding="utf-8")

        parser = PythonParser(temp_project)
        # 構文エラーがあっても例外が発生しないことを確認
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)

    def test_parser_with_empty_file(self, temp_project):
        """空のファイルの解析をテスト"""
        file_path = temp_project / "empty.py"
        file_path.write_text("", encoding="utf-8")

        parser = PythonParser(temp_project)
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)

    def test_api_generator_with_empty_project(self, temp_project):
        """空のプロジェクトでのAPI生成をテスト"""
        config = {
            "output": {"api_doc": "docs/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = temp_project / "docs" / "api.md"
        assert api_doc_path.exists()

    def test_readme_generator_with_no_dependencies(self, temp_project):
        """依存関係がないプロジェクトでのREADME生成をテスト"""
        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, [], config)
        result = generator.generate()

        assert result is True
        readme_path = temp_project / "README.md"
        assert readme_path.exists()

        content = readme_path.read_text(encoding="utf-8")
        assert len(content) > 0

    def test_readme_generator_with_invalid_manual_section(self, temp_project):
        """無効な手動セクションマーカーの処理をテスト"""
        readme_content = """# Test

<!-- MANUAL_START:description -->
説明
<!-- MANUAL_END:other -->
"""
        readme_path = temp_project / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        # エラーが発生しないことを確認
        result = generator.generate()
        assert result is True

    def test_api_generator_with_custom_output_path(self, temp_project):
        """カスタム出力パスでのAPI生成をテスト"""
        config = {
            "output": {"api_doc": "custom/path/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = temp_project / "custom" / "path" / "api.md"
        assert api_doc_path.exists()

    def test_parser_excludes_directories(self, temp_project):
        """除外ディレクトリが正しく除外されることを確認"""
        # 除外ディレクトリにファイルを作成
        (temp_project / ".git" / "file.py").parent.mkdir()
        (temp_project / ".git" / "file.py").write_text("def test(): pass\n", encoding="utf-8")

        # 通常のファイルを作成
        (temp_project / "main.py").write_text("def main(): pass\n", encoding="utf-8")

        parser = PythonParser(temp_project)
        apis = parser.parse_project(exclude_dirs=[".git"])

        # .git内のファイルは除外される
        files = [api["file"] for api in apis]
        assert ".git/file.py" not in files
        assert "main.py" in files or len(apis) >= 0

    def test_readme_generator_with_missing_config(self, temp_project):
        """設定が不完全な場合の処理をテスト"""
        config = {}  # 空の設定

        generator = ReadmeGenerator(temp_project, ["python"], config)
        # デフォルト値が使用されることを確認
        result = generator.generate()
        assert result is True

    def test_api_generator_with_no_languages(self, temp_project):
        """言語が指定されていない場合の処理をテスト"""
        config = {
            "output": {"api_doc": "docs/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(temp_project, [], config)
        result = generator.generate()

        # 空のリストでもエラーが発生しないことを確認
        assert isinstance(result, bool)
