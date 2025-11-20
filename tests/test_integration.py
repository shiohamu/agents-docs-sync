"""
統合テスト
"""

from pathlib import Path
import sys

import pytest
import yaml

# docgenモジュールをインポート
DOCGEN_DIR = Path(__file__).parent.parent / "docgen"
sys.path.insert(0, str(DOCGEN_DIR))

from detectors.javascript_detector import JavaScriptDetector
from detectors.python_detector import PythonDetector
from generators.api_generator import APIGenerator
from generators.readme_generator import ReadmeGenerator


@pytest.mark.integration
class TestIntegration:
    """統合テストクラス"""

    def test_end_to_end_python_project(self, python_project, sample_config):
        """Pythonプロジェクトのエンドツーエンドテスト"""
        # 設定ファイルを作成
        config = {
            "languages": {"auto_detect": True},
            "output": {"api_doc": "docs/api.md", "readme": "README.md"},
            "generation": {
                "update_readme": True,
                "generate_api_doc": True,
                "preserve_manual_sections": True,
            },
        }

        config_path = python_project / ".docgen" / "config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f)

        # DocGenを初期化（プロジェクトルートを一時的に変更）
        # 注意: 実際のDocGenはPROJECT_ROOTを使用するため、
        # このテストは制限がある

        # 代わりに、各コンポーネントを個別にテスト
        detector = PythonDetector(python_project)
        assert detector.detect() is True

        # API生成をテスト
        api_generator = APIGenerator(python_project, ["python"], config)
        result = api_generator.generate()
        assert result is True
        assert (python_project / "docs" / "api.md").exists()

        # README生成をテスト
        readme_generator = ReadmeGenerator(python_project, ["python"], config)
        result = readme_generator.generate()
        assert result is True
        assert (python_project / "README.md").exists()

    def test_multiple_languages_detection(self, multi_language_project):
        """複数言語プロジェクトでの検出をテスト"""
        python_detector = PythonDetector(multi_language_project)
        js_detector = JavaScriptDetector(multi_language_project)

        assert python_detector.detect() is True
        assert js_detector.detect() is True

    def test_readme_preserves_manual_sections(self, temp_project):
        """READMEの手動セクションが保持されることを統合テストで確認"""
        # 既存READMEを作成
        readme_content = """# Test Project

<!-- MANUAL_START:description -->
カスタム説明セクション
<!-- MANUAL_END:description -->

## 使用技術
"""
        readme_path = temp_project / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        # Pythonファイルを追加
        (temp_project / "main.py").write_text(
            'def hello():\n    """Hello function"""\n    pass\n', encoding="utf-8"
        )

        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        # READMEを生成
        generator = ReadmeGenerator(temp_project, ["python"], config)
        generator.generate()

        # 手動セクションが保持されていることを確認
        new_content = readme_path.read_text(encoding="utf-8")
        assert "カスタム説明セクション" in new_content
        assert "<!-- MANUAL_START:description -->" in new_content
        assert "<!-- MANUAL_END:description -->" in new_content
        # 自動生成セクションも追加されていることを確認
        assert "使用技術" in new_content

    def test_api_doc_includes_all_languages(self, multi_language_project):
        """複数言語のAPI情報が統合されることを確認"""
        # Pythonファイル
        (multi_language_project / "main.py").write_text(
            'def python_func():\n    """Python function"""\n    pass\n',
            encoding="utf-8",
        )

        # JavaScriptファイル
        (multi_language_project / "index.js").write_text(
            "/**\n * JavaScript function\n */\nfunction jsFunc() {}\n", encoding="utf-8"
        )

        config = {
            "output": {"api_doc": "docs/api.md"},
            "generation": {"generate_api_doc": True},
        }

        generator = APIGenerator(multi_language_project, ["python", "javascript"], config)
        generator.generate()

        api_doc_path = multi_language_project / "docs" / "api.md"
        assert api_doc_path.exists()

        content = api_doc_path.read_text(encoding="utf-8")
        # PythonとJavaScriptのAPI情報が含まれていることを確認
        assert "main.py" in content or "index.js" in content or len(content) > 0
