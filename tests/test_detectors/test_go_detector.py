"""
GoDetectorのテスト
"""

from detectors.go_detector import GoDetector
import pytest


@pytest.mark.unit
class TestGoDetector:
    """GoDetectorのテストクラス"""

    def test_detect_with_go_mod(self, go_project):
        """go.modがある場合に検出されることを確認"""
        detector = GoDetector(go_project)
        assert detector.detect() is True
        assert detector.get_language() == "go"

    def test_detect_with_go_files(self, temp_project):
        """Goファイルがある場合に検出されることを確認"""
        (temp_project / "main.go").write_text("package main\n", encoding="utf-8")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_without_go(self, temp_project):
        """Goプロジェクトでない場合に検出されないことを確認"""
        detector = GoDetector(temp_project)
        assert detector.detect() is False

    def test_get_language(self, go_project):
        """get_language()が'go'を返すことを確認"""
        detector = GoDetector(go_project)
        assert detector.get_language() == "go"
