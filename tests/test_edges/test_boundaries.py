"""Detector boundary tests (self-contained helper)"""

from pathlib import Path

from docgen.detectors.generic_detector import GenericDetector


def _write(root: Path, relative_path: str, content: str) -> Path:
    path = Path(root) / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def test_boundary_language_order_and_all_detected(temp_project):
    _write(temp_project, "main.rs", "fn main() {}\n")
    _write(temp_project, "Main.java", "public class Main {}\n")

    detector = GenericDetector(temp_project)
    assert detector.get_language() == "rust"

    detected = detector.get_all_detected_languages()
    assert "rust" in detected
    assert "java" in detected


def test_boundary_with_third_language(temp_project):
    _write(temp_project, "script.R", "# R code\n")
    _write(temp_project, "main.rs", "fn main() {}\n")
    _write(temp_project, "Main.java", "public class Main {}\n")
    detector = GenericDetector(temp_project)
    langs = set(detector.get_all_detected_languages())
    assert {"rust", "java", "r"}.issubset(langs)
