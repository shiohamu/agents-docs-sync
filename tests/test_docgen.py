"""
DocGenクラスのテスト
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.docgen import DocGen


class TestDocGen:
    """DocGenクラスのテスト"""

    def test_initialization_default(self, temp_project):
        """デフォルト設定での初期化テスト"""
        docgen = DocGen(project_root=temp_project)

        assert docgen.project_root == temp_project
        assert docgen.docgen_dir == temp_project / "docgen"
        assert docgen.config_path == temp_project / "docgen" / "config.yaml"
        assert isinstance(docgen.config, dict)
        assert docgen.detected_languages == []

    def test_initialization_with_config(self, temp_project):
        """設定ファイル指定での初期化テスト"""
        config_path = temp_project / "custom_config.yaml"
        config_path.write_text("""
output:
  agents_doc: CUSTOM_AGENTS.md
""")

        docgen = DocGen(project_root=temp_project, config_path=config_path)

        assert docgen.config_path == config_path
        assert docgen.config.get("output", {}).get("agents_doc") == "CUSTOM_AGENTS.md"

    def test_load_config_existing_file(self, temp_project):
        """既存の設定ファイル読み込みテスト"""
        config_file = temp_project / "docgen" / "config.yaml"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""
output:
  agents_doc: TEST_AGENTS.md
""")

        docgen = DocGen(project_root=temp_project)
        config = docgen._load_config()

        assert config["output"]["agents_doc"] == "TEST_AGENTS.md"

    def test_load_config_missing_file(self, temp_project):
        """設定ファイルが存在しない場合のテスト"""
        docgen = DocGen(project_root=temp_project)

        # _validate_configが呼ばれた後のconfigをチェック
        assert "languages" in docgen.config
        assert "output" in docgen.config
        assert "generation" in docgen.config
        assert "agents" in docgen.config

    def test_validate_config_missing_sections(self, temp_project):
        """設定セクションが不足している場合のテスト"""
        docgen = DocGen(project_root=temp_project)
        docgen.config = {}  # 空の設定

        docgen._validate_config()

        # デフォルト値がマージされる
        assert "languages" in docgen.config
        assert "output" in docgen.config
        assert "generation" in docgen.config

    def test_update_config(self, temp_project):
        """設定更新テスト"""
        docgen = DocGen(project_root=temp_project)

        updates = {"generation.update_readme": False, "output.agents_doc": "NEW_AGENTS.md"}

        docgen.update_config(updates)

        assert docgen.config["generation"]["update_readme"] is False
        assert docgen.config["output"]["agents_doc"] == "NEW_AGENTS.md"

    @patch("docgen.docgen.PythonDetector")
    @patch("docgen.docgen.JavaScriptDetector")
    @patch("docgen.docgen.GoDetector")
    @patch("docgen.docgen.GenericDetector")
    def test_detect_languages_parallel(
        self, mock_generic, mock_go, mock_js, mock_python, temp_project
    ):
        """並列言語検出テスト"""
        # モックの設定
        mock_python.return_value.detect.return_value = True
        mock_python.return_value.get_language.return_value = "python"
        mock_js.return_value.detect.return_value = False
        mock_go.return_value.detect.return_value = True
        mock_go.return_value.get_language.return_value = "go"
        mock_generic.return_value.detect.return_value = False

        docgen = DocGen(project_root=temp_project)
        languages = docgen.detect_languages(use_parallel=True)

        assert "python" in languages
        assert "go" in languages
        assert "javascript" not in languages
        assert docgen.detected_languages == languages

    @patch("docgen.docgen.PythonDetector")
    @patch("docgen.docgen.JavaScriptDetector")
    @patch("docgen.docgen.GoDetector")
    @patch("docgen.docgen.GenericDetector")
    def test_detect_languages_sequential(
        self, mock_generic, mock_go, mock_js, mock_python, temp_project
    ):
        """逐次言語検出テスト"""
        # モックの設定
        mock_python.return_value.detect.return_value = True
        mock_python.return_value.get_language.return_value = "python"
        mock_js.return_value.detect.return_value = False
        mock_go.return_value.detect.return_value = True
        mock_go.return_value.get_language.return_value = "go"
        mock_generic.return_value.detect.return_value = False

        docgen = DocGen(project_root=temp_project)
        languages = docgen.detect_languages(use_parallel=False)

        assert "python" in languages
        assert "go" in languages
        assert "javascript" not in languages

    @patch("docgen.docgen.APIGenerator")
    @patch("docgen.docgen.ReadmeGenerator")
    @patch("docgen.docgen.AgentsGenerator")
    def test_generate_documents_success(self, mock_agents, mock_readme, mock_api, temp_project):
        """ドキュメント生成成功テスト"""
        # モックの設定
        mock_api.return_value.generate.return_value = True
        mock_readme.return_value.generate.return_value = True
        mock_agents.return_value.generate.return_value = True

        docgen = DocGen(project_root=temp_project)
        docgen.detected_languages = ["python"]  # 言語を事前に設定

        result = docgen.generate_documents()

        assert result is True
        mock_api.assert_called_once()
        mock_readme.assert_called_once()
        mock_agents.assert_called_once()

    @patch("docgen.docgen.APIGenerator")
    @patch("docgen.docgen.ReadmeGenerator")
    @patch("docgen.docgen.AgentsGenerator")
    def test_generate_documents_partial_failure(
        self, mock_agents, mock_readme, mock_api, temp_project
    ):
        """ドキュメント生成一部失敗テスト"""
        # モックの設定
        mock_api.return_value.generate.return_value = True
        mock_readme.return_value.generate.return_value = False  # 失敗
        mock_agents.return_value.generate.return_value = True

        docgen = DocGen(project_root=temp_project)
        docgen.detected_languages = ["python"]

        result = docgen.generate_documents()

        assert result is False  # 一部失敗なのでFalse

    def test_generate_documents_no_languages(self, temp_project):
        """言語が検出されない場合のテスト"""
        docgen = DocGen(project_root=temp_project)
        docgen.detected_languages = []  # 言語なし

        with patch.object(docgen, "detect_languages", return_value=[]):
            result = docgen.generate_documents()

        assert result is False

    @patch("docgen.generators.commit_message_generator.CommitMessageGenerator")
    def test_main_commit_msg_command(self, mock_generator, temp_project, capsys):
        """commit-msgコマンドのテスト"""
        mock_generator.return_value.generate.return_value = "Test commit message"

        with patch("sys.argv", ["docgen.py", "commit-msg"]):
            with patch("docgen.DocGen", return_value=MagicMock()):
                from docgen import main as main_func

                exit_code = main_func()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Test commit message" in captured.out

    def test_main_detect_only(self, temp_project, caplog):
        """detect-onlyオプションのテスト"""
        with patch("sys.argv", ["docgen.py", "--detect-only"]):
            with patch("docgen.docgen.DocGen") as mock_docgen_class:
                mock_docgen = MagicMock()
                mock_docgen.detect_languages.return_value = ["python", "javascript"]
                mock_docgen_class.return_value = mock_docgen

                from docgen.docgen import main as main_func

                exit_code = main_func()

            assert exit_code == 0
            mock_docgen.detect_languages.assert_called_once()
