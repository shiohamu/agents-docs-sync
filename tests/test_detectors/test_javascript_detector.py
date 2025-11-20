"""JavaScriptDetectorのテスト（共通ヘルパー利用版）"""

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.detectors.javascript_detector import JavaScriptDetector


class TestJavaScriptDetector:
    """JavaScriptDetectorクラスのテスト"""

    def test_detect_with_package_json(self, temp_project):
        write_file(temp_project, "package.json", '{"name": "test"}')
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True

    def test_detect_with_js_files(self, temp_project):
        write_file(temp_project, "src/main.js", "console.log('hello');")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "javascript"

    def test_detect_with_ts_files(self, temp_project):
        write_file(temp_project, "src/script.ts", "const x: number = 1;")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "typescript"

    def test_detect_with_tsconfig_json(self, temp_project):
        write_file(temp_project, "tsconfig.json", "{}\n")
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is True
        assert detector.get_language() == "typescript"

    def test_detect_without_javascript(self, temp_project):
        detector = JavaScriptDetector(temp_project)
        assert detector.detect() is False

    def test_get_language_javascript(self, temp_project):
        write_file(temp_project, "package.json", '{"name": "test"}')
        detector = JavaScriptDetector(temp_project)
        assert detector.get_language() == "javascript"

    def test_get_language_typescript_with_tsconfig(self, temp_project):
        write_file(temp_project, "package.json", '{"name": "test"}')
        write_file(temp_project, "tsconfig.json", "{}")
        detector = JavaScriptDetector(temp_project)
        assert detector.get_language() == "typescript"

    def test_get_language_typescript_with_ts_files(self, temp_project):
        write_file(temp_project, "src/main.ts", "const x: number = 1")
        detector = JavaScriptDetector(temp_project)
        assert detector.get_language() == "typescript"

    def test_get_language_typescript_with_tsx_files(self, temp_project):
        write_file(
            temp_project, "src/component.tsx", "const Component: React.FC = () => <div></div>"
        )
        detector = JavaScriptDetector(temp_project)
        assert detector.get_language() == "typescript"
