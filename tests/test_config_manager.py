"""
ConfigManagerのテスト
"""

from pathlib import Path
from unittest.mock import patch

# docgenモジュールをインポート可能にする
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

from docgen.config_manager import ConfigManager


class TestConfigManager:
    """ConfigManagerクラスのテスト"""

    def test_config_manager_initialization_with_config_path(self, temp_project):
        """設定ファイルパス指定での初期化テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        config_path = docgen_dir / "custom_config.yaml"

        config_manager = ConfigManager(temp_project, docgen_dir, config_path)

        assert config_manager.project_root == temp_project
        assert config_manager.docgen_dir == docgen_dir
        assert config_manager.config_path == config_path

    def test_config_manager_initialization_default_config_path(self, temp_project):
        """デフォルト設定ファイルパスでの初期化テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        config_manager = ConfigManager(temp_project, docgen_dir)

        assert config_manager.config_path == docgen_dir / "config.yaml"

    @patch("docgen.config_manager.safe_read_yaml")
    def test_load_config_existing_file(self, mock_safe_read_yaml, temp_project):
        """既存の設定ファイル読み込みテスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        config_path = docgen_dir / "config.yaml"

        test_config = {"test": "value"}
        mock_safe_read_yaml.return_value = test_config

        config_manager = ConfigManager(temp_project, docgen_dir, config_path)

        assert config_manager.config == test_config
        mock_safe_read_yaml.assert_called_once_with(config_path)

    @patch("docgen.config_manager.safe_read_yaml")
    def test_load_config_nonexistent_file(self, mock_safe_read_yaml, temp_project):
        """存在しない設定ファイルのテスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        config_path = docgen_dir / "config.yaml"

        mock_safe_read_yaml.return_value = None

        with patch.object(
            ConfigManager, "_create_default_config", return_value={"default": "config"}
        ) as mock_default:
            config_manager = ConfigManager(temp_project, docgen_dir, config_path)

            assert config_manager.config == {"default": "config"}
            mock_default.assert_called_once()

    @patch("docgen.config_manager.safe_read_yaml")
    def test_create_default_config_with_sample(self, mock_safe_read_yaml, temp_project):
        """サンプル設定ファイルからのデフォルト設定作成テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        sample_path = docgen_dir / "config.yaml.sample"
        config_path = docgen_dir / "config.yaml"

        # サンプルファイルを作成
        sample_path.write_text("sample: config\n")

        mock_safe_read_yaml.side_effect = (
            lambda path: {"sample": "config"} if path == config_path else None
        )

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.docgen_dir = docgen_dir
        config_manager.config_path = config_path

        with patch.object(config_manager, "_copy_sample_config", return_value=True):
            result = config_manager._create_default_config()

            assert result == {"sample": "config"}

    @patch("docgen.config_manager.safe_read_yaml")
    def test_create_default_config_without_sample(self, mock_safe_read_yaml, temp_project):
        """サンプル設定ファイルなしの場合のデフォルト設定作成テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        config_path = docgen_dir / "config.yaml"

        mock_safe_read_yaml.return_value = None

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.docgen_dir = docgen_dir
        config_manager.config_path = config_path

        with patch.object(config_manager, "_copy_sample_config", return_value=False):
            with patch.object(
                config_manager, "_get_default_config", return_value={"default": "config"}
            ) as mock_default:
                result = config_manager._create_default_config()

                assert result == {"default": "config"}
                mock_default.assert_called_once()

    def test_copy_sample_config_success(self, temp_project):
        """サンプル設定ファイルのコピー成功テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        sample_path = docgen_dir / "config.yaml.sample"
        config_path = docgen_dir / "config.yaml"

        # サンプルファイルを作成
        sample_content = "sample: content"
        sample_path.write_text(sample_content)

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.config_path = config_path

        result = config_manager._copy_sample_config(sample_path)

        assert result is True
        assert config_path.exists()
        assert config_path.read_text() == sample_content

    def test_copy_sample_config_failure(self, temp_project):
        """サンプル設定ファイルのコピー失敗テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()
        sample_path = docgen_dir / "config.yaml.sample"
        config_path = docgen_dir / "config.yaml"

        # サンプルファイルを作成
        sample_path.write_text("content")

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.config_path = config_path

        # shutil.copy2をモックして例外を発生させる
        with patch("shutil.copy2", side_effect=Exception("Copy failed")):
            result = config_manager._copy_sample_config(sample_path)

            assert result is False

    def test_get_default_config(self, temp_project):
        """デフォルト設定の取得テスト"""
        config_manager = ConfigManager.__new__(ConfigManager)

        default_config = config_manager._get_default_config()

        # デフォルト設定に必要なキーが含まれていることを確認
        assert "output" in default_config
        assert "generation" in default_config
        assert "agents" in default_config
        assert "languages" in default_config

        # outputセクションの確認
        assert "agents_doc" in default_config["output"]
        assert "api_doc" in default_config["output"]
        assert "readme" in default_config["output"]

    def test_get_config(self, temp_project):
        """設定取得テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        test_config = {"test": "value"}
        with patch.object(ConfigManager, "_load_config", return_value=test_config):
            config_manager = ConfigManager(temp_project, docgen_dir)

            result = config_manager.get_config()
            assert result == test_config

    def test_update_config_simple(self, temp_project):
        """シンプルな設定更新テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.config = {"a": 1, "b": 2}

        config_manager.update_config("a", 3)

        assert config_manager.config["a"] == 3

    def test_update_config_nested(self, temp_project):
        """ネストされた設定更新テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        config_manager = ConfigManager.__new__(ConfigManager)
        config_manager.config = {"a": {"b": 2}}

        config_manager.update_config("a.b", 3)

        assert config_manager.config["a"]["b"] == 3

    def test_set_nested_value_existing(self, temp_project):
        """既存のネストされた値設定テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        config_manager = ConfigManager.__new__(ConfigManager)
        config = {"a": {"b": "old"}}

        config_manager._set_nested_value(config, ["a", "b"], "new")

        assert config["a"]["b"] == "new"

    def test_set_nested_value_new_structure(self, temp_project):
        """新規ネスト構造作成テスト"""
        docgen_dir = temp_project / ".docgen"
        docgen_dir.mkdir()

        config_manager = ConfigManager.__new__(ConfigManager)
        config = {}

        config_manager._set_nested_value(config, ["a", "b", "c"], "value")

        assert config["a"]["b"]["c"] == "value"
