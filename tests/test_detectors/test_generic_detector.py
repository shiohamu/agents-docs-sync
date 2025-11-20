"""
GenericDetectorのテスト
"""

from detectors.generic_detector import GenericDetector
import pytest


@pytest.mark.unit
class TestGenericDetector:
    """GenericDetectorのテストクラス"""

    def test_detect_rust(self, temp_project):
        """Rustファイルがある場合に検出されることを確認"""
        (temp_project / "main.rs").write_text("fn main() {}\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "rust"

    def test_detect_java(self, temp_project):
        """Javaファイルがある場合に検出されることを確認"""
        (temp_project / "Main.java").write_text("public class Main {}\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "java"

    def test_detect_ruby(self, temp_project):
        """Rubyファイルがある場合に検出されることを確認"""
        (temp_project / "main.rb").write_text("puts 'hello'\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "ruby"

    def test_detect_cpp(self, temp_project):
        """C++ファイルがある場合に検出されることを確認"""
        (temp_project / "main.cpp").write_text("int main() { return 0; }\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "cpp"

    def test_detect_without_supported_language(self, temp_project):
        """サポートされていない言語の場合に検出されないことを確認"""
        (temp_project / "file.txt").write_text("text\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        assert detector.detect() is False

    def test_get_all_detected_languages(self, temp_project):
        """複数言語が検出された場合にすべて返すことを確認"""
        (temp_project / "main.rs").write_text("fn main() {}\n", encoding="utf-8")
        (temp_project / "Main.java").write_text("public class Main {}\n", encoding="utf-8")
        detector = GenericDetector(temp_project)
        languages = detector.get_all_detected_languages()
        assert "rust" in languages
        assert "java" in languages
        assert len(languages) >= 2
