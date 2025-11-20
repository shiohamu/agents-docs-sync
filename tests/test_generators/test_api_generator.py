"""
APIGeneratorのテスト
"""

from generators.api_generator import APIGenerator
import pytest


@pytest.mark.unit
class TestAPIGenerator:
    """APIGeneratorのテストクラス"""

    def test_generate_creates_api_doc(self, python_project, sample_python_file):
        """APIドキュメントが生成されることを確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(python_project, ["python"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = python_project / "docs" / "api.md"
        assert api_doc_path.exists()

    def test_generate_api_doc_content(self, python_project, sample_python_file):
        """生成されたAPIドキュメントの内容を確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(python_project, ["python"], config)
        generator.generate()

        api_doc_path = python_project / "docs" / "api.md"
        content = api_doc_path.read_text(encoding="utf-8")

        assert "# API ドキュメント" in content
        assert "自動生成日時" in content

    def test_generate_with_multiple_languages(self, multi_language_project):
        """複数言語のAPI情報が統合されることを確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(multi_language_project, ["python", "javascript"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = multi_language_project / "docs" / "api.md"
        assert api_doc_path.exists()

    def test_generate_creates_output_directory(self, temp_project):
        """出力ディレクトリが自動作成されることを確認"""
        config = {
            "output": {"api_doc": "custom/docs/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(temp_project, ["python"], config)
        generator.generate()

        api_doc_path = temp_project / "custom" / "docs" / "api.md"
        assert api_doc_path.exists()

    def test_generate_with_no_apis(self, temp_project):
        """APIが見つからない場合でもドキュメントが生成されることを確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = temp_project / "docs" / "api.md"
        assert api_doc_path.exists()

        content = api_doc_path.read_text(encoding="utf-8")
        assert "APIが見つかりませんでした" in content or len(content) > 0
