"""
APIGeneratorのテスト
"""

import pytest

from docgen.generators.api_generator import APIGenerator
from tests.test_utils import assert_file_contains_text, assert_file_exists_and_not_empty


@pytest.mark.unit
class TestAPIGenerator:
    """APIGeneratorのテストクラス"""

    def test_initialization(self, api_generator):
        """APIGeneratorの初期化テスト"""
        assert api_generator.project_root.exists()
        assert api_generator.languages == ["python"]
        assert hasattr(api_generator, "config")

    def test_generate_creates_api_doc(self, api_generator, python_project, sample_python_file):
        """APIドキュメントが生成されることを確認"""
        result = api_generator.generate()

        assert result is True
        api_doc_path = api_generator.output_path
        assert_file_exists_and_not_empty(api_doc_path)

    def test_generate_api_doc_content(self, api_generator, python_project, sample_python_file):
        """生成されたAPIドキュメントの内容を確認"""
        api_generator.generate()

        api_doc_path = api_generator.output_path
        assert_file_contains_text(api_doc_path, "# API ドキュメント", "自動生成日時")

    def test_generate_with_multiple_languages(self, temp_project, multi_language_project):
        """複数言語のAPI情報が統合されることを確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(multi_language_project, ["python", "javascript"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = generator.output_path
        assert_file_exists_and_not_empty(api_doc_path)

    def test_generate_creates_output_directory(self, temp_project):
        """出力ディレクトリが自動作成されることを確認"""
        config = {
            "output": {"api_doc": "custom/docs/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(temp_project, ["python"], config)
        generator.generate()

        api_doc_path = generator.output_path
        assert_file_exists_and_not_empty(api_doc_path)

    def test_generate_with_no_apis(self, temp_project):
        """APIが見つからない場合でもドキュメントが生成されることを確認"""
        config = {"output": {"api_doc": "docs/api.md"}, "generation": {"generate_api_doc": True}}

        generator = APIGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        api_doc_path = generator.output_path
        assert_file_exists_and_not_empty(api_doc_path)

        content = api_doc_path.read_text(encoding="utf-8")
        # APIが見つからない場合でも基本的なドキュメントは生成される
        assert len(content.strip()) > 0
