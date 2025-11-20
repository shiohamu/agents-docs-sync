"""
PythonDetectorのテスト
"""

from detectors.python_detector import PythonDetector
import pytest


@pytest.mark.unit
class TestPythonDetector:
    """PythonDetectorのテストクラス"""

    def test_detect_with_requirements_txt(self, python_project):
        """requirements.txtがある場合に検出されることを確認"""
        detector = PythonDetector(python_project)
        assert detector.detect() is True
        assert detector.get_language() == "python"

    def test_detect_with_setup_py(self, temp_project):
        """setup.pyがある場合に検出されることを確認"""
        (temp_project / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_pyproject_toml(self, temp_project):
        """pyproject.tomlがある場合に検出されることを確認"""
        (temp_project / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_py_files(self, temp_project):
        """Pythonファイルがある場合に検出されることを確認"""
        (temp_project / "script.py").write_text("print('hello')\n", encoding="utf-8")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_without_python(self, temp_project):
        """Pythonプロジェクトでない場合に検出されないことを確認"""
        detector = PythonDetector(temp_project)
        assert detector.detect() is False

    def test_get_language(self, python_project):
        """get_language()が'python'を返すことを確認"""
        detector = PythonDetector(python_project)
        assert detector.get_language() == "python"
