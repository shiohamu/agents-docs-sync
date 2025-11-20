"""
ReadmeGeneratorのテスト
"""

from generators.readme_generator import ReadmeGenerator
import pytest


@pytest.mark.unit
class TestReadmeGenerator:
    """ReadmeGeneratorのテストクラス"""

    def test_generate_creates_readme(self, python_project):
        """READMEが生成されることを確認"""
        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(python_project, ["python"], config)
        result = generator.generate()

        assert result is True
        readme_path = python_project / "README.md"
        assert readme_path.exists()

    def test_generate_readme_content(self, python_project):
        """生成されたREADMEの内容を確認"""
        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(python_project, ["python"], config)
        generator.generate()

        readme_path = python_project / "README.md"
        content = readme_path.read_text(encoding="utf-8")

        assert "#" in content  # タイトルがある
        assert "使用技術" in content
        assert "Python" in content

    def test_extract_manual_sections(self, temp_project):
        """手動セクションが正しく抽出されることを確認"""
        readme_content = """# Test Project

<!-- MANUAL_START:description -->
これは手動で記述された説明です。
<!-- MANUAL_END:description -->

## 使用技術
"""
        readme_path = temp_project / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(temp_project, ["python"], config)
        sections = generator._extract_manual_sections(readme_content)

        assert "description" in sections
        assert "これは手動で記述された説明です。" in sections["description"]

    def test_preserve_manual_sections(self, temp_project):
        """手動セクションが保持されることを確認"""
        readme_content = """# Test Project

<!-- MANUAL_START:description -->
カスタム説明
<!-- MANUAL_END:description -->
"""
        readme_path = temp_project / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        generator.generate()

        new_content = readme_path.read_text(encoding="utf-8")
        assert "カスタム説明" in new_content
        assert "<!-- MANUAL_START:description -->" in new_content
        assert "<!-- MANUAL_END:description -->" in new_content

    def test_detect_dependencies_python(self, python_project):
        """Pythonの依存関係が検出されることを確認"""
        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(python_project, ["python"], config)
        dependencies = generator._detect_dependencies()

        assert "Python" in dependencies
        assert len(dependencies["Python"]) > 0

    def test_detect_dependencies_python_pep440_specifiers(self, temp_project):
        """PEP 440の様々なバージョン指定子が正しく処理されることを確認"""
        requirements_content = """requests==2.28.0
django>=4.0.0
flask<=2.3.0
numpy!=1.24.0
pandas~=2.0.0
pytest>7.0.0
setuptools<65.0.0
wheel===0.40.0
# コメント行
urllib3  # インラインコメント付き
"""
        (temp_project / "requirements.txt").write_text(requirements_content, encoding="utf-8")

        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(temp_project, ["python"], config)
        dependencies = generator._detect_dependencies()

        assert "Python" in dependencies
        deps = dependencies["Python"]

        # すべてのパッケージ名が正しく抽出されることを確認
        assert "requests" in deps
        assert "django" in deps
        assert "flask" in deps
        assert "numpy" in deps
        assert "pandas" in deps
        assert "pytest" in deps
        assert "setuptools" in deps
        assert "wheel" in deps
        assert "urllib3" in deps

        # バージョン指定子が含まれていないことを確認
        assert not any("!=" in dep for dep in deps)
        assert not any("~=" in dep for dep in deps)
        assert not any(">=" in dep for dep in deps)
        assert not any("<=" in dep for dep in deps)
        assert not any("==" in dep for dep in deps)
        assert not any(">" in dep for dep in deps)
        assert not any("<" in dep for dep in deps)

        # コメント行が含まれていないことを確認
        assert "コメント行" not in str(deps)

    def test_detect_dependencies_javascript(self, javascript_project):
        """JavaScriptの依存関係が検出されることを確認"""
        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(javascript_project, ["javascript"], config)
        dependencies = generator._detect_dependencies()

        assert "Node.js" in dependencies
        assert len(dependencies["Node.js"]) > 0

    def test_detect_dependencies_go_multiline_require(self, temp_project):
        """Goの複数行requireブロックの依存関係が検出されることを確認"""
        go_mod_content = """module test-project

go 1.20

require (
    github.com/pkg/errors v0.9.1
    github.com/stretchr/testify v1.7.0
    golang.org/x/sync v0.1.0
)

require github.com/example/single v1.0.0
"""
        (temp_project / "go.mod").write_text(go_mod_content, encoding="utf-8")

        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(temp_project, ["go"], config)
        dependencies = generator._detect_dependencies()

        assert "Go" in dependencies
        go_deps = dependencies["Go"]
        # 複数行ブロック内の依存関係が検出されることを確認
        assert "github.com/pkg/errors" in go_deps
        assert "github.com/stretchr/testify" in go_deps
        assert "golang.org/x/sync" in go_deps
        # 単一行のrequireも検出されることを確認
        assert "github.com/example/single" in go_deps
        assert len(go_deps) >= 4

    def test_get_project_structure(self, python_project):
        """プロジェクト構造が生成されることを確認"""
        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(python_project, ["python"], config)
        structure = generator._get_project_structure()

        assert isinstance(structure, list)
        assert len(structure) > 0

    def test_get_project_structure_excludes_files(self, temp_project):
        """プロジェクト構造から除外ファイルが除外されることを確認"""
        # 除外されるファイルを作成
        (temp_project / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
        (temp_project / ".gitattributes").write_text("* text=auto\n", encoding="utf-8")

        # 通常のファイルを作成
        (temp_project / "main.py").write_text("print('hello')\n", encoding="utf-8")
        (temp_project / "README.md").write_text("# Test\n", encoding="utf-8")

        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(temp_project, ["python"], config)
        structure = generator._get_project_structure()

        structure_str = "\n".join(structure)

        # 除外ファイルが含まれていないことを確認
        assert ".gitignore" not in structure_str
        assert ".gitattributes" not in structure_str

        # 通常のファイルは含まれていることを確認
        assert "main.py" in structure_str or "README.md" in structure_str

    def test_get_project_structure_excludes_dirs(self, temp_project):
        """プロジェクト構造から除外ディレクトリが除外されることを確認"""
        # 除外されるディレクトリを作成
        (temp_project / ".git").mkdir()
        (temp_project / ".git" / "config").write_text("[core]\n", encoding="utf-8")
        (temp_project / "__pycache__").mkdir()
        (temp_project / "__pycache__" / "test.pyc").write_bytes(b"\x00")

        # 通常のディレクトリを作成
        (temp_project / "src").mkdir()
        (temp_project / "src" / "main.py").write_text("print('hello')\n", encoding="utf-8")

        config = {"generation": {"preserve_manual_sections": True}}

        generator = ReadmeGenerator(temp_project, ["python"], config)
        structure = generator._get_project_structure()

        structure_str = "\n".join(structure)

        # 除外ディレクトリが含まれていないことを確認
        assert ".git" not in structure_str
        assert "__pycache__" not in structure_str

        # 通常のディレクトリは含まれていることを確認
        assert "src" in structure_str

    def test_generate_with_manual_sections(self, temp_project):
        """複数の手動セクションが保持されることを確認"""
        readme_content = """# Test

<!-- MANUAL_START:description -->
説明
<!-- MANUAL_END:description -->

<!-- MANUAL_START:setup -->
セットアップ手順
<!-- MANUAL_END:setup -->
"""
        readme_path = temp_project / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        config = {
            "output": {"readme": "README.md"},
            "generation": {"update_readme": True, "preserve_manual_sections": True},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        generator.generate()

        new_content = readme_path.read_text(encoding="utf-8")
        assert "説明" in new_content
        assert "セットアップ手順" in new_content
