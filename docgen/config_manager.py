"""
設定管理モジュール
"""

from pathlib import Path
import shutil
from typing import Any

try:
    from .utils.logger import get_logger
    from .utils.file_utils import safe_read_yaml
except ImportError:
    from utils.logger import get_logger
    from utils.file_utils import safe_read_yaml

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
        else:
            # 設定ファイルが存在しない場合、sampleからコピーを試みる
            sample_path = self.docgen_dir / "config.yaml.sample"
            if sample_path.exists():
                try:
                    shutil.copy2(sample_path, self.config_path)
                    logger.info(f"{sample_path.name}から{self.config_path.name}を作成しました。")
                    config = safe_read_yaml(self.config_path)
                    return config if config is not None else self._get_default_config()
                except Exception as e:
                    logger.warning(f"設定ファイルの作成に失敗しました: {e}")
                    logger.info("デフォルト設定を使用します。")
            else:
                logger.warning(f"設定ファイルが見つかりません: {self.config_path}")
                logger.info("デフォルト設定を使用します。")
            return self._get_default_config()

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
        }

    def get_config(self) -> dict[str, Any]:
        """現在の設定を取得"""
        return self.config

    def update_config(self, key: str, value: Any):
        """設定を更新"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
