"""PythonDetectorのテスト（共通ヘルパー利用版）"""

import pytest

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.detectors.python_detector import PythonDetector


class TestPythonDetector:
    def test_detect_with_requirements_txt(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "python"

    def test_detect_with_setup_py(self, temp_project):
        write_file(temp_project, "setup.py", "from setuptools import setup\nsetup(name='test')\n")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_pyproject_toml(self, temp_project):
        write_file(temp_project, "pyproject.toml", '[build-system]\nrequires = ["setuptools"]\n')
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_py_files(self, temp_project):
        write_file(temp_project, "script.py", "print('hello')\n")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_without_python(self, temp_project):
        detector = PythonDetector(temp_project)
        assert detector.detect() is False

    def test_get_language(self, temp_project):
        detector = PythonDetector(temp_project)
        assert detector.get_language() == "python"

    def test_detect_package_manager_uv(self, temp_project):
        write_file(temp_project, "uv.lock", "# uv lock file")
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "uv"

    def test_detect_package_manager_poetry(self, temp_project):
        write_file(temp_project, "poetry.lock", "# poetry lock file")
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "poetry"

    def test_detect_package_manager_poetry_pyproject(self, temp_project):
        write_file(temp_project, "pyproject.toml", '[tool.poetry]\nname = "test"\n')
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "poetry"

    def test_detect_package_manager_conda(self, temp_project):
        write_file(temp_project, "environment.yml", "name: test\n")
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "conda"

    def test_detect_package_manager_pip_requirements(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0")
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "pip"

    def test_detect_package_manager_pip_setup_py(self, temp_project):
        write_file(temp_project, "setup.py", "from setuptools import setup\nsetup(name='test')\n")
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() == "pip"

    def test_detect_package_manager_none(self, temp_project):
        detector = PythonDetector(temp_project)
        assert detector.detect_package_manager() is None

    def test_detect_with_nested_python_files(self, temp_project):
        write_file(temp_project, "src/package/sub/module.py", "def func(): pass\n")
        detector = PythonDetector(temp_project)
        assert detector.detect() is True

    def test_detect_ignores_symlinks(self, temp_project, monkeypatch):
        real_file = temp_project / "real.py"
        write_file(temp_project, "real.py", "print('real')")

        try:
            link_file = temp_project / "link.py"
            link_file.symlink_to(real_file)
        except OSError:
            pytest.skip("Symlinks not supported on this platform")

        detector = PythonDetector(temp_project)
        assert detector.detect() is True
