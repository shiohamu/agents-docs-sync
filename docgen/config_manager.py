"""
設定管理モジュール
"""

from pathlib import Path
import shutil
from typing import Any

from .utils.file_utils import safe_read_yaml
from .utils.logger import get_logger

logger = get_logger("config_manager")


class ConfigManager:
    """設定ファイルの管理クラス"""

    def __init__(self, project_root: Path, docgen_dir: Path, config_path: Path | None = None):
        """
        初期化

        Args:
            project_root: プロジェクトルートパス
            docgen_dir: .docgenディレクトリパス
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        self.project_root = project_root
        self.docgen_dir = docgen_dir
        self.config_path = config_path or self.docgen_dir / "config.yaml"
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """
        設定ファイルを読み込む

        Returns:
            設定辞書。ファイルが存在しない場合はデフォルト設定を返す
        """
        config = safe_read_yaml(self.config_path)
        if config is not None:
            return config

        return self._create_default_config()

    def _create_default_config(self) -> dict[str, Any]:
        """デフォルト設定を作成して返す"""
        sample_path = self.docgen_dir / "config.yaml.sample"
        if sample_path.exists():
            if self._copy_sample_config(sample_path):
                config = safe_read_yaml(self.config_path)
                return config if config is not None else self._get_default_config()

        logger.warning(f"設定ファイルが見つかりません: {self.config_path}")
        logger.info("デフォルト設定を使用します。")
        return self._get_default_config()

    def _copy_sample_config(self, sample_path: Path) -> bool:
        """サンプル設定ファイルをコピー"""
        try:
            shutil.copy2(sample_path, self.config_path)
            logger.info(f"{sample_path.name}から{self.config_path.name}を作成しました。")
            return True
        except Exception as e:
            logger.error(f"設定ファイルの作成に失敗しました: {e}", exc_info=True)
            logger.info("デフォルト設定を使用します。")
            return False

    def _get_default_config(self) -> dict[str, Any]:
        """デフォルト設定を返す"""
        return {
            "languages": {"auto_detect": True, "preferred": []},
            "output": {
                "api_doc": "docs/api.md",
                "readme": "README.md",
                "agents_doc": "AGENTS.md",
            },
            "generation": {
                "update_readme": True,
                "generate_api_doc": True,
                "generate_agents_doc": True,
                "preserve_manual_sections": True,
            },
            "agents": {
                "llm_mode": "both",
                "generation": {
                    "agents_mode": "template",
                    "readme_mode": "template",
                    "enable_commit_message": True,
                },
            },
        }

    def get_config(self) -> dict[str, Any]:
        """現在の設定を取得"""
        return self.config

    def update_config(self, key: str, value: Any):
        """設定を更新"""
        keys = key.split(".")
        self._set_nested_value(self.config, keys, value)

    def _set_nested_value(self, config: dict[str, Any], keys: list[str], value: Any):
        """ネストされた辞書に値を設定"""
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value
