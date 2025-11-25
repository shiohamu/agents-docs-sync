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

    def test_generate_readme_with_llm(self, temp_project, monkeypatch):
        # LLMを使用する場合のテスト（モックを使用）
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")

        # LLMクライアントをモック（ローカルLLMとして設定）
        from unittest.mock import MagicMock, Mock, patch

        mock_client = Mock()
        mock_client.generate.return_value = """# Test Project

<!-- MANUAL_START:description -->
This is an LLM generated description.
<!-- MANUAL_END:description -->

## 使用技術

- Python

## 依存関係

### Python
- pytest>=7.0.0

## セットアップ

<!-- MANUAL_START:setup -->
## Prerequisites

- Python 3.12以上

## Installation

### Python

```bash
pip install -r requirements.txt
```

## LLM環境のセットアップ

### APIを使用する場合

1. **APIキーの取得と設定**

   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください

<!-- MANUAL_END:setup -->

---

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 15:56:23*"""
        # ローカルLLMとして設定
        mock_client.provider = "lmstudio"
        mock_client.base_url = "http://192.168.10.113:1234"
        mock_client.model = "openai/gpt-oss-20b"
        mock_client.generate = MagicMock(return_value="This is an LLM generated description.")

        with (
            patch(
                "docgen.generators.base_generator.BaseGenerator._get_llm_client_with_fallback",
                return_value=mock_client,
            ),
            patch(
                "docgen.generators.base_generator.BaseGenerator._generate_with_outlines",
                return_value="# Test Project\n\nThis is an LLM generated description.\n\n## Technologies Used\n\n- Python\n",
            ),
        ):
            config = {
                "output": {"readme": "README.md"},
                "agents": {"generation": {"readme_mode": "llm"}},
            }

            generator = ReadmeGenerator(temp_project, ["python"], config)
            result = generator.generate()

            assert result is True
            assert (temp_project / "README.md").exists()

            content = (temp_project / "README.md").read_text(encoding="utf-8")
            # LLM生成の場合は手動セクションをマージしないので、LLMのdescriptionが適用される
            assert "This is an LLM generated description." in content

    def test_create_overview_prompt(self, temp_project):
        """概要プロンプト作成のテスト"""
        config = {"output": {"readme": "README.md"}}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        # プロジェクト情報を作成
        from docgen.models.project import ProjectInfo

        project_info = ProjectInfo(
            description="Test project",
            dependencies={"python": ["pytest"]},
            build_commands=["python setup.py build"],
            test_commands=["pytest"],
        )

        existing_overview = "This is existing overview."

        prompt = generator._create_overview_prompt(project_info, existing_overview)

        assert "プロジェクト情報:" in prompt
        assert "Test project" in prompt
        assert "This is existing overview." in prompt
        assert "改善されたプロジェクト概要の内容をマークダウン形式で出力してください。" in prompt

    def test_generate_overview_with_llm_success(self, temp_project, monkeypatch):
        """概要LLM生成成功のテスト"""
        config = {"output": {"readme": "README.md"}}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        # プロジェクト情報を作成
        from docgen.models.project import ProjectInfo

        project_info = ProjectInfo(description="Test project")

        # LLMクライアントをモック
        from unittest.mock import Mock

        mock_client = Mock()
        mock_client.generate.return_value = "Improved overview content."

        monkeypatch.setattr(generator, "_get_llm_client_with_fallback", lambda: mock_client)
        monkeypatch.setattr(generator, "_clean_llm_output", lambda x: x)
        monkeypatch.setattr(generator, "_validate_output", lambda x: True)

        result = generator._generate_overview_with_llm(project_info, "existing overview")

        assert result == "Improved overview content."
        mock_client.generate.assert_called_once()

    def test_generate_overview_with_llm_failure(self, temp_project, monkeypatch):
        """概要LLM生成失敗のテスト"""
        config = {"output": {"readme": "README.md"}}
        generator = ReadmeGenerator(temp_project, ["python"], config)

        # プロジェクト情報を作成
        from docgen.models.project import ProjectInfo

        project_info = ProjectInfo(description="Test project")

        # LLMクライアントがNoneの場合
        monkeypatch.setattr(generator, "_get_llm_client_with_fallback", lambda: None)

        existing_overview = "existing overview"
        result = generator._generate_overview_with_llm(project_info, existing_overview)

        assert result is None

    def test_generate_hybrid_readme(self, temp_project, monkeypatch):
        """ハイブリッドモードのテスト"""
        write_file(temp_project, "requirements.txt", "pytest>=7.0.0\n")

        config = {
            "output": {"readme": "README.md"},
            "agents": {"generation": {"readme_mode": "hybrid"}},
        }

        generator = ReadmeGenerator(temp_project, ["python"], config)

        # LLMで改善された概要を返すようにモック
        def mock_generate_overview(project_info, existing_overview):
            return "LLM improved overview content."

        monkeypatch.setattr(generator, "_generate_overview_with_llm", mock_generate_overview)

        result = generator.generate()

        assert result is True
        assert (temp_project / "README.md").exists()

        content = (temp_project / "README.md").read_text(encoding="utf-8")
        assert "LLM improved overview content." in content
