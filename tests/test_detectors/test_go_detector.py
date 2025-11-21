"""GoDetectorのテスト（共通ヘルパー利用版）"""

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.detectors.go_detector import GoDetector


class TestGoDetector:
    """GoDetectorクラスのテスト"""

    def test_detect_with_go_mod(self, temp_project):
        write_file(temp_project, "go.mod", "module example.com/test")
        detector = GoDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "go"

    def test_detect_with_go_sum(self, temp_project):
        write_file(temp_project, "go.sum", "")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_gopkg_toml(self, temp_project):
        write_file(temp_project, "Gopkg.toml", "")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_gopkg_lock(self, temp_project):
        write_file(temp_project, "Gopkg.lock", "")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_glide_yaml(self, temp_project):
        write_file(temp_project, "glide.yaml", "")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_glide_lock(self, temp_project):
        write_file(temp_project, "glide.lock", "")
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_package_manager_go_modules(self, temp_project):
        write_file(temp_project, "go.mod", "module example.com/test")
        detector = GoDetector(temp_project)
        assert detector.detect_package_manager() == "go"

    def test_detect_package_manager_dep(self, temp_project):
        write_file(temp_project, "Gopkg.toml", "")
        detector = GoDetector(temp_project)
        assert detector.detect_package_manager() == "dep"

    def test_detect_package_manager_glide(self, temp_project):
        write_file(temp_project, "glide.yaml", "")
        detector = GoDetector(temp_project)
        assert detector.detect_package_manager() == "glide"

    def test_detect_package_manager_none(self, temp_project):
        detector = GoDetector(temp_project)
        assert detector.detect_package_manager() is None

    def test_detect_with_go_files(self, temp_project):
        write_file(
            temp_project,
            "main.go",
            'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Hello")\n}\n',
        )
        detector = GoDetector(temp_project)
        assert detector.detect() is True

    def test_detect_without_go_files(self, temp_project):
        detector = GoDetector(temp_project)
        assert detector.detect() is False

    def test_get_language(self, temp_project):
        detector = GoDetector(temp_project)
        assert detector.get_language() == "go"
