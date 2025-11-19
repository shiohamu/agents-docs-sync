"""
CommitMessageGeneratorのテスト
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from generators.commit_message_generator import CommitMessageGenerator  # pyright: ignore[reportMissingImports]


class TestCommitMessageGenerator:
    """CommitMessageGeneratorクラスのテスト"""

    def test_initialization(self, temp_project):
        """初期化テスト"""
        config = {"agents": {"llm_mode": "api"}}
        generator = CommitMessageGenerator(temp_project, config)

        assert generator.project_root == temp_project
        assert generator.config == config
        assert generator.agents_config == {"llm_mode": "api"}

    def test_initialization_empty_config(self, temp_project):
        """空の設定での初期化テスト"""
        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        assert generator.agents_config == {}

    @patch("generators.commit_message_generator.subprocess.run")
    def test_get_staged_changes_success(self, mock_subprocess, temp_project):
        """ステージング済み変更の取得成功テスト"""
        # git diff --cached --stat のモック
        stat_result = Mock()
        stat_result.returncode = 0
        stat_result.stdout = "file.py | 5 +-\n1 file changed, 5 insertions(+)"

        # git diff --cached のモック
        diff_result = Mock()
        diff_result.returncode = 0
        diff_result.stdout = "+ new line\n- old line"

        mock_subprocess.side_effect = [stat_result, diff_result]

        config = {}
        generator = CommitMessageGenerator(temp_project, config)
        result = generator._get_staged_changes()

        assert result is not None
        assert "file.py | 5 +-" in result
        assert "+ new line" in result

        # subprocess.runが2回呼ばれたことを確認
        assert mock_subprocess.call_count == 2

    @patch("generators.commit_message_generator.subprocess.run")
    def test_get_staged_changes_no_changes(self, mock_subprocess, temp_project):
        """ステージング済み変更がない場合のテスト"""
        # git diff --cached --stat のモック
        stat_result = Mock()
        stat_result.returncode = 0
        stat_result.stdout = ""

        # git diff --cached のモック
        diff_result = Mock()
        diff_result.returncode = 0
        diff_result.stdout = ""

        mock_subprocess.side_effect = [stat_result, diff_result]

        config = {}
        generator = CommitMessageGenerator(temp_project, config)
        result = generator._get_staged_changes()

        assert result == "\n\n"

    @patch("generators.commit_message_generator.subprocess.run")
    def test_get_staged_changes_git_error(self, mock_subprocess, temp_project):
        """Gitコマンドエラーのテスト"""
        result_mock = Mock()
        result_mock.returncode = 1
        result_mock.stderr = "fatal: not a git repository"
        mock_subprocess.return_value = result_mock

        config = {}
        generator = CommitMessageGenerator(temp_project, config)
        result = generator._get_staged_changes()

        assert result is None

    def test_get_staged_changes_no_git(self, temp_project, monkeypatch):
        """Gitコマンドが存在しない場合のテスト"""

        def mock_subprocess_run(*args, **kwargs):
            raise FileNotFoundError("git command not found")

        monkeypatch.setattr(
            "generators.commit_message_generator.subprocess.run", mock_subprocess_run
        )

        config = {}
        generator = CommitMessageGenerator(temp_project, config)
        result = generator._get_staged_changes()

        assert result is None

    def test_create_prompt(self, temp_project):
        """プロンプト作成テスト"""
        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        staged_changes = "file.py | 2 +-\n+ new feature"
        prompt = generator._create_prompt(staged_changes)

        assert "以下のGitの変更内容を分析して" in prompt
        assert staged_changes in prompt
        assert "Conventional Commits形式" in prompt
        assert "コミットメッセージを1行で生成" in prompt

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_success(self, mock_create_client, temp_project):
        """コミットメッセージ生成成功テスト"""
        # LLMクライアントのモック
        mock_client = Mock()
        mock_client.generate.return_value = "feat: add new feature"
        mock_create_client.return_value = mock_client

        config = {"agents": {"llm_mode": "api"}}
        generator = CommitMessageGenerator(temp_project, config)

        # ステージング済み変更取得のモック
        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        assert result == "feat: add new feature"
        mock_create_client.assert_called_once()
        mock_client.generate.assert_called_once()

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_no_staged_changes(self, mock_create_client, temp_project):
        """ステージング済み変更がない場合のテスト"""
        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        # ステージング済み変更がない場合
        with patch.object(generator, "_get_staged_changes", return_value=None):
            result = generator.generate()

        assert result is None
        mock_create_client.assert_not_called()

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_no_client(self, mock_create_client, temp_project):
        """LLMクライアント作成失敗のテスト"""
        mock_create_client.return_value = None

        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        assert result is None

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_llm_returns_none(self, mock_create_client, temp_project):
        """LLMがNoneを返す場合のテスト"""
        mock_client = Mock()
        mock_client.generate.return_value = None
        mock_create_client.return_value = mock_client

        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        assert result is None

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_llm_returns_multiline(self, mock_create_client, temp_project):
        """LLMが複数行のメッセージを返す場合のテスト"""
        mock_client = Mock()
        mock_client.generate.return_value = (
            "feat: add new feature\n\nThis is a detailed description"
        )
        mock_create_client.return_value = mock_client

        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        assert result == "feat: add new feature"

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_exception_handling(self, mock_create_client, temp_project):
        """例外発生時のテスト"""
        mock_client = Mock()
        mock_client.generate.side_effect = Exception("Test error")
        mock_create_client.return_value = mock_client

        config = {}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        assert result is None

    @patch(
        "generators.commit_message_generator.LLMClientFactory.create_client_with_fallback"
    )
    def test_generate_with_local_fallback(self, mock_create_client, temp_project):
        """ローカルLLMへのフォールバックテスト"""
        mock_client = Mock()
        mock_client.generate.return_value = "fix: bug fix"
        mock_create_client.return_value = mock_client

        config = {"agents": {"llm_mode": "local"}}
        generator = CommitMessageGenerator(temp_project, config)

        with patch.object(
            generator, "_get_staged_changes", return_value="test changes"
        ):
            result = generator.generate()

        # preferred_mode='local'で呼び出されたことを確認
        mock_create_client.assert_called_once_with(
            {"llm_mode": "local"}, preferred_mode="local"
        )
        assert result == "fix: bug fix"
