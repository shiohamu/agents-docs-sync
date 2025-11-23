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

    def __init__(
        self,
        project_root: Path,
        docgen_dir: Path,
        config_path: Path | None = None,
        package_config_sample: Path | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトルートパス
            docgen_dir: .docgenディレクトリパス
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
            package_config_sample: パッケージ内のサンプル設定ファイルパス
        """
        self.project_root = project_root
        self.docgen_dir = docgen_dir
        self.config_path = config_path or self.docgen_dir / "config.yaml"
        self._package_config_sample = package_config_sample
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> dict[str, Any]:
        """
        設定ファイルを読み込む

        Returns:
            設定辞書。ファイルが存在しない場合はデフォルト設定を返す
        """
        if self.config_path.exists():
            config = safe_read_yaml(self.config_path)
            if config is not None:
                return config
            else:
                logger.warning("設定ファイルの読み込みに失敗しました")
                logger.info("デフォルト設定を使用します。")
                return self._get_default_config()
        else:
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

    def _set_nested_value(self, config: dict[str, Any], keys: list[str], value: Any):
        """ネストされた辞書に値を設定"""
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def _validate_config(self) -> None:
        """
        設定の妥当性を検証

        Raises:
            ValueError: 設定が無効な場合
        """
        # 必須フィールドのチェック
        required_sections = ["languages", "output", "generation"]
        for section in required_sections:
            if section not in self.config:
                logger.warning(
                    f"設定セクション '{section}' がありません。デフォルト値を使用します。"
                )
                # デフォルトをマージ
                default = self._get_default_config()
                self.config[section] = default.get(section, {})

        # outputパスの検証
        output_config = self.config.get("output", {})
        for key, path in output_config.items():
            if not isinstance(path, str):
                logger.warning(
                    f"output.{key} は文字列である必要があります。デフォルト値を使用します。"
                )
                default = self._get_default_config()["output"][key]
                self.config["output"][key] = default

        # generationフラグの検証
        generation_config = self.config.get("generation", {})
        for key, value in generation_config.items():
            if not isinstance(value, bool):
                logger.warning(
                    f"generation.{key} はブール値である必要があります。デフォルト値を使用します。"
                )
                default = self._get_default_config()["generation"][key]
                self.config["generation"][key] = default

    def update_config(self, updates: dict[str, Any]) -> None:
        """
        設定を動的に更新

        Args:
            updates: 更新する設定辞書（ドット記法対応、例: {'generation.update_readme': False}）
        """

        def set_nested_value(d: dict[str, Any], keys: list[str], value: Any) -> None:
            for key in keys[:-1]:
                d = d.setdefault(key, {})
            d[keys[-1]] = value

        for key_path, value in updates.items():
            keys = key_path.split(".")
            set_nested_value(self.config, keys, value)

        # 更新後に再検証
        self._validate_config()
        logger.info(f"設定を更新しました: {updates}")
