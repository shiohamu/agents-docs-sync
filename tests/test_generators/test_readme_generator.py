"""ReadmeGeneratorのテスト（共通ヘルパー利用版）"""

from pathlib import Path
import sys

# Resolve repo root for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from test_utils.common import write_file
except Exception:
    from pathlib import Path as _Path

    def write_file(root, relative_path, content):
        path = _Path(root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path


from docgen.generators.readme_generator import ReadmeGenerator


class TestReadmeGenerator:
    """ReadmeGeneratorクラスのテスト"""

    def test_readme_generator_initialization(self, temp_project):
        config = {"output": {"readme": "README.md"}}
        generator = ReadmeGenerator(temp_project, ["python"], config)
        assert generator.project_root == temp_project
        assert generator.languages == ["python"]
        assert generator.config == config
        assert generator.readme_path == temp_project / "README.md"

    def test_generate_readme_without_llm(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")
        write_file(
            temp_project,
            "setup.py",
            """
from setuptools import setup
setup(
  name=\"test-project\",
  description=\"A test project\",
  install_requires=[\"pytest\"]
)
""",
        )

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert temp_project.name in content

    def test_generate_readme_empty_project(self, temp_project):
        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, [], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "#" in content  # タイトルが含まれていること

    def test_generate_readme_multiple_languages(self, temp_project):
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")
        write_file(temp_project, "package.json", '{"name": "test-project", "version": "1.0.0"}')

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python", "javascript"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "#" in content

    def test_generate_readme_with_project_info_error(self, temp_project):
        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        # 空プロジェクトでもREADMEは生成されるはず
        assert result is True
        assert (temp_project / "README.md").exists()

    def test_extract_manual_sections(self, temp_project):
        generator = ReadmeGenerator(temp_project, ["python"], {})

        content = """
# Project

<!-- MANUAL_START:description -->
This is a manual description.
<!-- MANUAL_END:description -->

## Installation

<!-- MANUAL_START:custom -->
Custom section content.
<!-- MANUAL_END:custom -->
"""

        sections = generator._extract_manual_sections(content)

        assert sections["description"] == "This is a manual description."
        assert sections["custom"] == "Custom section content."

    def test_extract_manual_sections_empty(self, temp_project):
        generator = ReadmeGenerator(temp_project, ["python"], {})

        content = """
# Project

## Installation

Normal content without manual sections.
"""

        sections = generator._extract_manual_sections(content)
        assert sections == {}

    def test_generate_readme_custom_output_path(self, temp_project):
        config = {
            "output": {"readme": "CUSTOM.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": False},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True
        assert (temp_project / "CUSTOM.md").exists()

    def test_generate_readme_preserve_manual_sections(self, temp_project):
        existing_readme = """
# Project

<!-- MANUAL_START:description -->
This is a manual description that should be preserved.
<!-- MANUAL_END:description -->

## Installation

Standard installation instructions.
"""
        (temp_project / "README.md").write_text(existing_readme)

        config = {
            "output": {"readme": "README.md"},
            "readme": {"use_llm": False, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator.generate()

        assert result is True

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "This is a manual description that should be preserved." in content
