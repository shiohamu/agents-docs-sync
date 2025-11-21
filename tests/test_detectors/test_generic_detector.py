"""GenericDetectorのテスト（共通ヘルパー利用版）"""

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.detectors.generic_detector import GenericDetector


class TestGenericDetector:
    def test_detect_rust(self, temp_project):
        write_file(temp_project, "main.rs", "fn main() {}\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "rust"

    def test_detect_java(self, temp_project):
        write_file(temp_project, "Main.java", "public class Main {}\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "java"

    def test_detect_ruby(self, temp_project):
        write_file(temp_project, "main.rb", "puts 'hello'\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "ruby"

    def test_detect_cpp(self, temp_project):
        write_file(temp_project, "main.cpp", "int main() { return 0; }\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "cpp"

    def test_detect_without_supported_language(self, temp_project):
        write_file(temp_project, "file.txt", "text\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is False

    def test_detect_package_manager_none(self, temp_project):
        detector = GenericDetector(temp_project)
        assert detector.detect_package_manager() is None

    def test_get_all_detected_languages(self, temp_project):
        write_file(temp_project, "main.rs", "fn main() {}\n")
        write_file(temp_project, "Main.java", "public class Main {}\n")
        detector = GenericDetector(temp_project)
        languages = detector.get_all_detected_languages()
        assert "rust" in languages
        assert "java" in languages

    def test_get_language_returns_first_detected(self, temp_project):
        write_file(temp_project, "main.java", "// java code\n")
        write_file(temp_project, "main.c", "// c code\n")
        detector = GenericDetector(temp_project)
        assert detector.get_language() == "java"

    def test_detect_with_header_files(self, temp_project):
        write_file(temp_project, "header.h", "// c header\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "c"

    def test_detect_case_insensitive_extensions(self, temp_project):
        write_file(temp_project, "script.R", "# R code\n")
        detector = GenericDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "r"
