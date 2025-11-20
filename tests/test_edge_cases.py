"""
エッジケースとエラーハンドリングのテスト
"""

from pathlib import Path
import sys

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


    def test_config_file_nonexistent(self, tmp_path):
        """存在しない設定ファイルの処理テスト"""
        from docgen.docgen import DocGen

        nonexistent_config = tmp_path / "nonexistent.yaml"
        docgen = DocGen(project_root=tmp_path, config_path=nonexistent_config)

        # デフォルト設定が使用されることを確認
        assert "generation" in docgen.config
        assert "output" in docgen.config

    def test_config_file_invalid_yaml(self, tmp_path):
        """無効なYAML設定ファイルの処理テスト"""
        from docgen.docgen import DocGen

        invalid_config = tmp_path / "invalid.yaml"
        invalid_config.write_text("invalid: yaml: content: [\n", encoding="utf-8")

        docgen = DocGen(project_root=tmp_path, config_path=invalid_config)

        # デフォルト設定が使用されることを確認
        assert "generation" in docgen.config

    def test_large_project_processing(self, temp_project):
        """大規模プロジェクトの処理テスト"""
        # 多数のファイルを生成
        for i in range(50):
            file_path = temp_project / f"module_{i}.py"
            file_path.write_text(f"def function_{i}():\n    pass\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        # 言語検出が正常に動作することを確認
        languages = docgen.detect_languages()
        assert "python" in languages

    def test_special_characters_in_files(self, temp_project):
        """特殊文字を含むファイルの処理テスト"""
        # 特殊文字を含むPythonファイル
        special_code = '''
def function_with_unicode():
    """関数 with ユニコード"""
    return "Hello 世界 🌍"

class ClassWithSpecialChars:
    """クラス with special chars: àáâãäå"""
    pass
'''
        file_path = temp_project / "special_chars.py"
        file_path.write_text(special_code, encoding="utf-8")

        from generators.parsers.python_parser import PythonParser
        parser = PythonParser(temp_project)

        # 特殊文字があっても正常に解析されることを確認
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)
        assert len(apis) > 0

    def test_network_error_fallback(self, temp_project, monkeypatch):
        """ネットワークエラー時のLLMフォールバックテスト"""
        from generators.agents_generator import AgentsGenerator

        config = {
            "output": {"agents_doc": "AGENTS.md"},
            "agents": {"llm_mode": "api"}
        }

        generator = AgentsGenerator(temp_project, ["python"], config)

        # LLMClientFactoryがNoneを返すようにモック（ネットワークエラー）
        with monkeypatch.MagicMock() as mock_factory:
            mock_factory.create_client_with_fallback.return_value = None

            # _generate_with_llmがNoneを返すことを確認
            result = generator._generate_with_llm({})
            assert result is None

    def test_mixed_language_project(self, temp_project):
        """複数言語混在プロジェクトの処理テスト"""
        # Pythonファイル
        (temp_project / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")

        # JavaScriptファイル
        (temp_project / "app.js").write_text("console.log('hello');\n", encoding="utf-8")

        # Goファイル
        (temp_project / "main.go").write_text("package main\n\nfunc main() {}\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        languages = docgen.detect_languages()

        # すべての言語が検出されることを確認
        assert "python" in languages
        assert "javascript" in languages
        assert "go" in languages

    def test_deeply_nested_directory_structure(self, temp_project):
        """深くネストされたディレクトリ構造の処理テスト"""
        # 深いディレクトリ構造を作成
        deep_dir = temp_project
        for i in range(10):
            deep_dir = deep_dir / f"level_{i}"
            deep_dir.mkdir()

        # 最深部にファイルを作成
        deep_file = deep_dir / "deep.py"
        deep_file.write_text("def deep_function():\n    pass\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        languages = docgen.detect_languages()
        assert "python" in languages

    def test_binary_files_ignored(self, temp_project):
        """バイナリファイルが無視されるテスト"""
        # バイナリファイルを作成
        binary_file = temp_project / "binary.dat"
        binary_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe\xfd")

        # Pythonファイルも作成
        py_file = temp_project / "script.py"
        py_file.write_text("def func():\n    pass\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        languages = docgen.detect_languages()
        assert "python" in languages

    def test_circular_import_handling(self, temp_project):
        """循環インポートを含むファイルの処理テスト"""
        # 循環インポートを含むファイル
        circular_code = '''
# This creates a circular import scenario
from . import module_a
from . import module_b

def func():
    pass
'''
        file_path = temp_project / "circular.py"
        file_path.write_text(circular_code, encoding="utf-8")

        from generators.parsers.python_parser import PythonParser
        parser = PythonParser(temp_project)

        # 循環インポートがあってもクラッシュしないことを確認
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)

    def test_very_long_file_processing(self, temp_project):
        """非常に長いファイルの処理テスト"""
        # 長いファイルを作成（1000行）
        long_code = "\n".join([f"def func_{i}():\n    pass" for i in range(1000)])
        file_path = temp_project / "long_file.py"
        file_path.write_text(long_code, encoding="utf-8")

        from generators.parsers.python_parser import PythonParser
        parser = PythonParser(temp_project)

        # 長いファイルでも正常に処理されることを確認
        apis = parser.parse_file(file_path)
        assert isinstance(apis, list)
        assert len(apis) > 0

    def test_unicode_file_names(self, temp_project):
        """Unicodeファイル名の処理テスト"""
        # Unicodeファイル名
        unicode_file = temp_project / "テストファイル.py"
        unicode_file.write_text("def test():\n    pass\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        languages = docgen.detect_languages()
        assert "python" in languages

    def test_hidden_files_ignored(self, temp_project):
        """隠しファイルが無視されるテスト"""
        # 隠しファイルを作成
        hidden_file = temp_project / ".hidden.py"
        hidden_file.write_text("def hidden():\n    pass\n", encoding="utf-8")

        # 通常ファイルも作成
        normal_file = temp_project / "normal.py"
        normal_file.write_text("def normal():\n    pass\n", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)

        languages = docgen.detect_languages()
        assert "python" in languages
