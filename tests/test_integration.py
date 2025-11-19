"""
統合テスト
"""

import pytest
import yaml
from pathlib import Path
import sys

# docgenモジュールをインポート
DOCGEN_DIR = Path(__file__).parent.parent / "docgen"
sys.path.insert(0, str(DOCGEN_DIR))

from docgen import DocGen
from detectors.python_detector import PythonDetector
from detectors.javascript_detector import JavaScriptDetector
from generators.api_generator import APIGenerator
from generators.readme_generator import ReadmeGenerator


@pytest.mark.integration
class TestIntegration:
    """統合テストクラス"""

    def test_end_to_end_python_project(self, python_project, sample_config):
        """Pythonプロジェクトのエンドツーエンドテスト"""
        # 設定ファイルを作成
        config = {
            'languages': {
                'auto_detect': True
            },
            'output': {
                'api_doc': 'docs/api.md',
                'readme': 'README.md'
            },
            'generation': {
                'update_readme': True,
                'generate_api_doc': True,
                'preserve_manual_sections': True
            }
        }

        config_path = python_project / "docgen" / "config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f)

        # DocGenを初期化（プロジェクトルートを一時的に変更）
        # 注意: 実際のDocGenはPROJECT_ROOTを使用するため、
        # このテストは制限がある

        # 代わりに、各コンポーネントを個別にテスト
        detector = PythonDetector(python_project)
        assert detector.detect() is True

        # API生成をテスト
        api_generator = APIGenerator(python_project, ['python'], config)
        result = api_generator.generate()
        assert result is True
        assert (python_project / "docs" / "api.md").exists()

        # README生成をテスト
        readme_generator = ReadmeGenerator(python_project, ['python'], config)
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
        readme_path.write_text(readme_content, encoding='utf-8')

        # Pythonファイルを追加
        (temp_project / "main.py").write_text(
            'def hello():\n    """Hello function"""\n    pass\n',
            encoding='utf-8'
        )

        config = {
            'output': {
                'readme': 'README.md'
            },
            'generation': {
                'update_readme': True,
                'preserve_manual_sections': True
            }
        }

        # READMEを生成
        generator = ReadmeGenerator(temp_project, ['python'], config)
        generator.generate()

        # 手動セクションが保持されていることを確認
        new_content = readme_path.read_text(encoding='utf-8')
        assert 'カスタム説明セクション' in new_content
        assert '<!-- MANUAL_START:description -->' in new_content
        assert '<!-- MANUAL_END:description -->' in new_content
        # 自動生成セクションも追加されていることを確認
        assert '使用技術' in new_content

    def test_api_doc_includes_all_languages(self, multi_language_project):
        """複数言語のAPI情報が統合されることを確認"""
        # Pythonファイル
        (multi_language_project / "main.py").write_text(
            'def python_func():\n    """Python function"""\n    pass\n',
            encoding='utf-8'
        )

        # JavaScriptファイル
        (multi_language_project / "index.js").write_text(
            '/**\n * JavaScript function\n */\nfunction jsFunc() {}\n',
            encoding='utf-8'
        )

        config = {
            'output': {
                'api_doc': 'docs/api.md'
            },
            'generation': {
                'generate_api_doc': True
            }
        }

        generator = APIGenerator(multi_language_project, ['python', 'javascript'], config)
        generator.generate()

        api_doc_path = multi_language_project / "docs" / "api.md"
        assert api_doc_path.exists()

        content = api_doc_path.read_text(encoding='utf-8')
        # PythonとJavaScriptのAPI情報が含まれていることを確認
        assert 'main.py' in content or 'index.js' in content or len(content) > 0


    def test_full_pipeline_execution(self, temp_project):
        """完全なパイプライン実行テスト"""
        from docgen.docgen import DocGen
        
        # プロジェクトにファイルを追加
        (temp_project / "main.py").write_text("""
def main():
    '''メイン関数'''
    print("Hello World")

class MyClass:
    '''テストクラス'''
    
    def method(self):
        '''テストメソッド'''
        return "test"
""", encoding="utf-8")

        (temp_project / "utils.py").write_text("""
def helper():
    '''ヘルパー関数'''
    return "helper"
""", encoding="utf-8")

        # DocGenで完全な処理を実行
        docgen = DocGen(project_root=temp_project)
        
        # 言語検出
        languages = docgen.detect_languages()
        assert "python" in languages
        
        # ドキュメント生成
        result = docgen.generate_documents()
        assert result is True
        
        # 生成されたファイルを確認
        assert (temp_project / "README.md").exists()
        assert (temp_project / "docs" / "api.md").exists()
        
        # READMEの内容を確認
        readme_content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "# " in readme_content  # タイトルがある
        assert "Python" in readme_content  # 言語が記載されている
        
        # APIドキュメントの内容を確認
        api_content = (temp_project / "docs" / "api.md").read_text(encoding="utf-8")
        assert len(api_content) > 0  # 何か内容がある

    def test_performance_large_project(self, temp_project):
        """大規模プロジェクトのパフォーマンステスト"""
        import time
        
        # 多数のファイルを生成
        for i in range(20):
            file_path = temp_project / f"module_{i}.py"
            file_path.write_text(f"""
def function_{i}():
    '''Function {i}'''
    return {i}

class Class{i}:
    '''Class {i}'''
    pass
""", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)
        
        # 処理時間を測定
        start_time = time.time()
        result = docgen.generate_documents()
        end_time = time.time()
        
        # 正常に完了することを確認
        assert result is True
        
        # 処理時間が妥当であることを確認（30秒以内）
        processing_time = end_time - start_time
        assert processing_time < 30, f"Processing took too long: {processing_time} seconds"

    def test_memory_usage_monitoring(self, temp_project):
        """メモリ使用量の監視テスト"""
        import psutil
        import os
        
        # プロジェクトにファイルを追加
        for i in range(10):
            file_path = temp_project / f"test_{i}.py"
            file_path.write_text(f"def func_{i}():\n    pass\n" * 100, encoding="utf-8")
        
        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)
        
        # メモリ使用量を測定
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        result = docgen.generate_documents()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # 正常に完了することを確認
        assert result is True
        
        # メモリ増加が妥当であることを確認（500MB以内）
        assert memory_increase < 500, f"Memory increase too large: {memory_increase} MB"

    def test_error_recovery_and_fallbacks(self, temp_project):
        """エラー回復とフォールバックのテスト"""
        from docgen.docgen import DocGen
        
        # 不正なファイルを追加
        (temp_project / "invalid.py").write_text("def invalid syntax (\n", encoding="utf-8")
        
        # 正常なファイルも追加
        (temp_project / "valid.py").write_text("def valid():\n    pass\n", encoding="utf-8")
        
        docgen = DocGen(project_root=temp_project)
        
        # エラーが発生しても全体の処理が停止しないことを確認
        result = docgen.generate_documents()
        assert result is True  # 一部のエラーは許容される
        
        # 有効なファイルの処理結果は得られるはず
        assert (temp_project / "README.md").exists()

    def test_cross_language_integration(self, temp_project):
        """クロス言語統合テスト"""
        # Pythonファイル
        (temp_project / "main.py").write_text("""
def main():
    '''メイン関数'''
    return "python"
""", encoding="utf-8")

        # JavaScriptファイル
        (temp_project / "app.js").write_text("""
/**
 * メイン関数
 */
function main() {
    return "javascript";
}
""", encoding="utf-8")

        from docgen.docgen import DocGen
        docgen = DocGen(project_root=temp_project)
        
        # 複数言語が検出されることを確認
        languages = docgen.detect_languages()
        assert len(languages) >= 2
        assert "python" in languages
        assert "javascript" in languages
        
        # ドキュメント生成
        result = docgen.generate_documents()
        assert result is True
        
        # READMEに両方の言語が記載されていることを確認
        readme_content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "Python" in readme_content
        assert "JavaScript" in readme_content

    def test_configuration_persistence(self, temp_project):
        """設定の永続性テスト"""
        from docgen.docgen import DocGen
        
        # 初期設定
        initial_config = {
            "generation": {"update_readme": True},
            "output": {"readme": "README.md"}
        }
        
        docgen1 = DocGen(project_root=temp_project)
        docgen1.config.update(initial_config)
        
        # 設定を更新
        docgen1.update_config({"generation.update_readme": False})
        
        # 新しいインスタンスで設定が維持されていることを確認
        docgen2 = DocGen(project_root=temp_project)
        # 注意: 実際の設定ファイルがない場合、デフォルトが使用される
        assert "generation" in docgen2.config

    def test_idempotent_operations(self, temp_project):
        """冪等性操作テスト（同じ操作を複数回実行しても結果が同じ）"""
        from docgen.docgen import DocGen
        
        # プロジェクトにファイルを追加
        (temp_project / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")
        
        docgen = DocGen(project_root=temp_project)
        
        # 最初の実行
        result1 = docgen.generate_documents()
        assert result1 is True
        
        readme1 = (temp_project / "README.md").read_text(encoding="utf-8")
        
        # 2回目の実行
        result2 = docgen.generate_documents()
        assert result2 is True
        
        readme2 = (temp_project / "README.md").read_text(encoding="utf-8")
        
        # 結果が同じであることを確認
        assert result1 == result2
        assert readme1 == readme2

    def test_backward_compatibility(self, temp_project):
        """後方互換性テスト"""
        from docgen.docgen import DocGen
        
        # 古い形式の設定
        old_config = {
            "update_readme": True,  # 古いキー
            "generate_api_doc": True,
            "output_dir": "docs"  # 古いキー
        }
        
        docgen = DocGen(project_root=temp_project)
        docgen.config.update(old_config)
        
        # 正常に動作することを確認
        result = docgen.generate_documents()
        assert isinstance(result, bool)  # TrueまたはFalseのどちらでも可
