"""
ReadmeGeneratorのテスト
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from generators.readme_generator import ReadmeGenerator, ReadmeDocument


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
        readme_path = readme_generator.readme_path
        assert_file_exists_and_not_empty(readme_path)

    def test_generate_readme_content(self, readme_generator, python_project):
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

    def test_should_use_outlines_enabled_readme(self, temp_project):
        """ReadmeGenerator Outlines使用判定テスト - 有効"""
        config = {
            "generation": {"preserve_manual_sections": True},
            "use_outlines": True,
        }
        generator = ReadmeGenerator(temp_project, ["python"], config)
        assert generator._should_use_outlines() is True

    def test_should_use_outlines_disabled_readme(self, temp_project):
        """ReadmeGenerator Outlines使用判定テスト - 無効"""
        config = {
            "generation": {"preserve_manual_sections": True},
            "use_outlines": False,
        }
        generator = ReadmeGenerator(temp_project, ["python"], config)
        assert generator._should_use_outlines() is False

    def test_readme_document_creation(self):
        """ReadmeDocumentの作成テスト"""
        data = {
            "title": "Test Project",
            "description": "Test description",
            "technologies": ["Python"],
            "dependencies": {"Python": ["pytest>=7.0.0"]},
            "setup_instructions": {
                "prerequisites": ["Python 3.12"],
                "installation_steps": ["pip install -r requirements.txt"],
            },
            "project_structure": ["src/", "tests/"],
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest tests/"],
            "manual_sections": {},
        }

        doc = ReadmeDocument(**data)
        assert doc.title == "Test Project"
        assert doc.description == "Test description"
        assert doc.technologies == ["Python"]
        assert doc.dependencies == {"Python": ["pytest>=7.0.0"]}
        assert doc.setup_instructions == {
            "prerequisites": ["Python 3.12"],
            "installation_steps": ["pip install -r requirements.txt"],
        }
        assert doc.project_structure == ["src/", "tests/"]
        assert doc.build_commands == ["python setup.py build"]
        assert doc.test_commands == ["pytest tests/"]
        assert doc.manual_sections == {}

    def test_convert_readme_structured_data_to_markdown(self, temp_project):
        """README構造化データからマークダウン変換テスト"""
        config = {"generation": {"preserve_manual_sections": True}}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        data = ReadmeDocument(
            title="Test Project",
            description="Test description",
            technologies=["Python"],
            dependencies={"Python": ["pytest>=7.0.0"]},
            setup_instructions={
                "prerequisites": ["Python 3.12"],
                "installation_steps": ["pip install -r requirements.txt"],
            },
            project_structure=["src/", "tests/"],
            build_commands=["python setup.py build"],
            test_commands=["pytest tests/"],
            manual_sections={},
        )

        manual_sections = {}
        markdown = generator._convert_readme_structured_data_to_markdown(
            data, manual_sections
        )

        assert "# Test Project" in markdown
        assert "Test description" in markdown
        assert "Python" in markdown
        assert "pytest>=7.0.0" in markdown
        assert "Python 3.12" in markdown
        assert "src/" in markdown
        assert "python setup.py build" in markdown
        assert "pytest tests/" in markdown

    @patch("utils.outlines_utils.OUTLINES_AVAILABLE", True)
    def test_generate_with_outlines_readme_success(self, temp_project):
        """README Outlines生成成功テスト"""
        from unittest.mock import Mock

        # Mock Outlines
        mock_model = Mock()
        mock_model.return_value = ReadmeDocument(
            title="Test Project",
            description="Test description",
            technologies=["Python"],
            dependencies={"Python": ["pytest>=7.0.0"]},
            setup_instructions={
                "prerequisites": ["Python 3.12"],
                "installation_steps": ["pip install -r requirements.txt"],
            },
            project_structure=["src/", "tests/"],
            build_commands=["python setup.py build"],
            test_commands=["pytest tests/"],
            manual_sections={},
        )

        config = {
            "generation": {"preserve_manual_sections": True},
            "use_outlines": True,
            "agents": {
                "llm_mode": "api",
                "api": {"provider": "openai", "model": "gpt-4o"},
            },
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)

        with patch.object(
            generator, "_create_outlines_model_readme", return_value=mock_model
        ):
            result = generator._generate_with_outlines_readme({})

            assert result is not None
            assert "# Test Project" in result
            assert "Test description" in result

    @patch("utils.outlines_utils.OUTLINES_AVAILABLE", False)
    def test_generate_with_outlines_readme_fallback(self, temp_project):
        """README Outlines生成フォールバックテスト"""
        config = {
            "generation": {"preserve_manual_sections": True},
            "use_outlines": True,
            "agents": {"llm_mode": "api"},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)
        result = generator._generate_with_outlines_readme({})

        # Outlinesが利用できないため、従来の生成にフォールバック
        assert result is not None
        assert "# " in result  # プロジェクト名を含むタイトル

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
        (temp_project / "requirements.txt").write_text(
            requirements_content, encoding="utf-8"
        )

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
        (temp_project / "src" / "main.py").write_text(
            "print('hello')\n", encoding="utf-8"
        )

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

    def test_format_project_info_for_prompt(self, temp_project):
        """プロジェクト情報フォーマットテスト"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        project_info = {
            "description": "Test project description",
            "dependencies": {"python": ["pytest", "requests"]},
            "build_commands": ["python setup.py build"],
            "test_commands": ["pytest tests/"],
        }

        result = generator._format_project_info_for_readme_prompt(project_info)

        assert "説明: Test project description" in result
        assert "依存関係:" in result
        assert "python: pytest, requests" in result
        assert "ビルドコマンド:" in result
        assert "python setup.py build" in result
        assert "テストコマンド:" in result
        assert "pytest tests/" in result

    def test_format_manual_sections_for_prompt(self, temp_project):
        """手動セクションのプロンプトフォーマットテスト"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        manual_sections = {
            "Installation": "pip install package",
            "Usage": "import package; package.do_something()",
        }

        result = generator._format_manual_sections_for_prompt(manual_sections)

        assert "Installation: pip install package..." in result
        assert "Usage: import package; package.do_something()..." in result

    def test_format_manual_sections_for_prompt_empty(self, temp_project):
        """空の手動セクションのプロンプトフォーマットテスト"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        result = generator._format_manual_sections_for_prompt({})

        assert result == "なし"

    def test_convert_readme_structured_data_to_markdown(self, temp_project):
        """構造化データをマークダウンに変換テスト"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        data = ReadmeDocument(
            title="Test Project",
            description="A test project",
            technologies=["Python", "pytest"],
            dependencies={"python": ["pytest>=7.0.0"]},
            setup_instructions={"prerequisites": ["Python 3.8+"]},
            project_structure=["src/", "tests/"],
            build_commands=["python setup.py build"],
            test_commands=["pytest"],
            manual_sections={"custom": "Custom content"},
        )

        manual_sections = {"existing": "Existing content"}

        result = generator._convert_readme_structured_data_to_markdown(
            data, manual_sections
        )

        assert "# Test Project" in result
        assert "A test project" in result
        assert "Python, pytest" in result
        assert "pytest>=7.0.0" in result
        assert "Python 3.8+" in result
        assert "src/, tests/" in result
        assert "python setup.py build" in result
        assert "pytest" in result
        assert "Custom content" in result
        assert "Existing content" in result

    def test_detect_dependencies_python_new(self, temp_project):
        """Python依存関係検出テスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        # requirements.txtを作成
        (temp_project / "requirements.txt").write_text(
            "pytest>=7.0.0\nrequests==2.28.0\n"
        )

        result = generator._detect_dependencies()

        assert "Python" in result
        assert "pytest>=7.0.0" in result["Python"]
        assert "requests==2.28.0" in result["Python"]

    def test_detect_dependencies_javascript_new(self, temp_project):
        """JavaScript依存関係検出テスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["javascript"], config)

        # package.jsonを作成
        import json

        package_data = {"dependencies": {"express": "^4.18.0", "lodash": "~4.17.21"}}
        (temp_project / "package.json").write_text(
            json.dumps(package_data), encoding="utf-8"
        )

        result = generator._detect_dependencies()

        assert "Node.js" in result
        assert "express@^4.18.0" in result["Node.js"]
        assert "lodash@~4.17.21" in result["Node.js"]

    def test_detect_dependencies_go_new(self, temp_project):
        """Go依存関係検出テスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["go"], config)

        # go.modを作成
        (temp_project / "go.mod").write_text(
            "module test\n\ngo 1.20\n\nrequire github.com/stretchr/testify v1.8.0\n"
        )

        result = generator._detect_dependencies()

        assert "Go" in result
        assert "github.com/stretchr/testify v1.8.0" in result["Go"]

    def test_detect_dependencies_empty_new(self, temp_project):
        """依存関係なしの場合のテスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        result = generator._detect_dependencies()

        assert result == {}

    @patch("generators.readme_generator.LLMClientFactory.create_client_with_fallback")
    def test_generate_with_outlines_success_readme_new(
        self, mock_create_client, temp_project
    ):
        """Outlinesを使用したREADME生成成功テスト（新規）"""
        mock_client = Mock()
        mock_client.generate.return_value = '{"title": "Test", "description": "Test project", "technologies": ["Python"], "dependencies": {}, "setup_instructions": {}, "project_structure": [], "build_commands": [], "test_commands": [], "manual_sections": {}}'
        # JSONをパースしてReadmeDocumentを作成
        import json

        data = json.loads(mock_client.generate.return_value)
        mock_document = ReadmeDocument(**data)
        mock_create_client.return_value = mock_client

        config = {
            "output": {"readme": "README.md"},
            "use_outlines": True,
            "agents": {"llm_mode": "api"},
        }
        generator = ReadmeGenerator(temp_project, ["python"], config)

        result = generator._generate_with_outlines_readme({})

        assert result is not None
        assert "# Test" in result
        assert "Test project" in result

    @patch("generators.readme_generator.LLMClientFactory.create_client_with_fallback")
    def test_generate_with_outlines_fallback_readme_new(
        self, mock_create_client, temp_project
    ):
        """Outlines生成失敗時のフォールバックテスト（新規）"""
        mock_create_client.return_value = None

        config = {"output": {"readme": "README.md"}, "use_outlines": True}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        result = generator._generate_with_outlines_readme({})

        assert result is not None  # フォールバック生成が動作

    def test_extract_manual_sections_new(self, temp_project):
        """手動セクション抽出テスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        content = """# Project

Auto generated content

<!-- MANUAL_START:installation -->
pip install package
<!-- MANUAL_END:installation -->

More auto content

<!-- MANUAL_START:usage -->
import package
<!-- MANUAL_END:usage -->
"""

        result = generator._extract_manual_sections(content)

        assert "installation" in result
        assert "pip install package" in result["installation"]
        assert "usage" in result
        assert "import package" in result["usage"]

    def test_extract_manual_sections_no_manual_new(self, temp_project):
        """手動セクションなしの場合のテスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        content = "# Project\n\nJust auto generated content"

        result = generator._extract_manual_sections(content)

        assert result == {}

    def test_preserve_manual_sections_new(self, temp_project):
        """手動セクション保持テスト（新規）"""
        config = {}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        new_content = """# Project

New auto content

<!-- MANUAL_START:installation -->
pip install package
<!-- MANUAL_END:installation -->
"""

        manual_sections = {"usage": "import package"}

        result = generator._preserve_manual_sections_in_generated(
            new_content, manual_sections
        )

        assert "<!-- MANUAL_START:installation -->" in result
        assert "<!-- MANUAL_END:installation -->" in result
        assert "<!-- MANUAL_START:usage -->" in result
        assert "<!-- MANUAL_END:usage -->" in result
        assert "import package" in result
