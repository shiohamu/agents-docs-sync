"""
ConfigManagerのテスト
"""

from unittest.mock import patch

import pytest

from docgen.config_manager import ConfigManager
from tests.test_utils import create_config_file


class TestConfigManager:
    """ConfigManagerのテストクラス"""

    def test_initialization(self, config_manager):
        """ConfigManagerの初期化テスト"""
        assert config_manager.project_root.exists()
        assert hasattr(config_manager, "config_path")
        assert hasattr(config_manager, "get_config")

    def test_load_config_success(self, temp_project):
        """設定ファイルの読み込み成功"""
        config_data = {"test": "value", "nested": {"key": "value"}}
        config_path = create_config_file(temp_project, config_data)

        manager = ConfigManager(temp_project, temp_project, config_path)
        assert manager.get_config() == config_data

    def test_load_config_invalid_yaml(self, temp_project):
        """無効なYAMLファイルの場合、デフォルト設定を使用"""
        config_path = temp_project / "config.yaml"
        config_path.write_text("invalid: yaml: content: [\n", encoding="utf-8")

        manager = ConfigManager(temp_project, temp_project, config_path)
        config = manager.get_config()

        # デフォルト設定が返されることを確認
        assert "languages" in config
        assert "output" in config
        assert "generation" in config

    def test_get_default_config(self, temp_project):
        """デフォルト設定の内容を確認"""
        manager = ConfigManager(temp_project, temp_project)
        default_config = manager._get_default_config()

        expected_keys = ["languages", "output", "generation"]
        for key in expected_keys:
            assert key in default_config

        assert default_config["output"]["api_doc"] == "docs/api.md"
        assert default_config["output"]["readme"] == "README.md"
        assert default_config["output"]["agents_doc"] == "AGENTS.md"

    @pytest.mark.parametrize(
        "key,value",
        [
            ("test_key", "test_value"),
            ("nested.key", "nested_value"),
            ("deep.nested.key", "deep_value"),
        ],
    )
    def test_update_config(self, temp_project, key, value):
        """設定更新のテスト（パラメータ化）"""
        manager = ConfigManager(temp_project, temp_project)
        manager.update_config(key, value)

        config = manager.get_config()
        keys = key.split(".")
        for k in keys[:-1]:
            config = config[k]
        assert config[keys[-1]] == value

    @patch("docgen.config_manager.safe_read_yaml")
    def test_load_config_read_failure(self, mock_read_yaml, temp_project):
        """設定ファイル読み込み失敗"""
        mock_read_yaml.return_value = None

        manager = ConfigManager(temp_project, temp_project)
        config = manager.get_config()

        # デフォルト設定が返されることを確認
        assert "languages" in config
