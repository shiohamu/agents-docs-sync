"""
JavaScriptDetectorのテスト
"""

from detectors.javascript_detector import JavaScriptDetector
import pytest


@pytest.mark.unit
class TestJavaScriptDetector:
    """JavaScriptDetectorのテストクラス"""

    def test_detect_with_package_json(self, javascript_project):
        """package.jsonがある場合に検出されることを確認"""
        detector = JavaScriptDetector(javascript_project)
        assert detector.detect() is True

    def test_detect_with_js_files(self, temp_project):
        """JavaScriptファイルがある場合に検出されることを確認"""
        (temp_project / "script.js").write_text("console.log('hello');\n", encoding="utf-8")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "javascript"

    def test_detect_with_ts_files(self, temp_project):
        """TypeScriptファイルがある場合にTypeScriptとして検出されることを確認"""
        (temp_project / "script.ts").write_text("const x: number = 1;\n", encoding="utf-8")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "typescript"

    def test_detect_with_tsconfig_json(self, temp_project):
        """tsconfig.jsonがある場合に検出されることを確認"""
        (temp_project / "tsconfig.json").write_text("{}\n", encoding="utf-8")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "typescript"

    def test_detect_without_javascript(self, temp_project):
        """JavaScriptプロジェクトでない場合に検出されないことを確認"""
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is False

    def test_get_language_javascript(self, javascript_project):
        """JavaScriptプロジェクトの場合に'javascript'を返すことを確認"""
        detector = JavaScriptDetector(javascript_project)
        assert detector.get_language() == "javascript"
