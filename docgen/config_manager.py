"""
設定管理モジュール
"""

import logging
from pathlib import Path
import shutil
from typing import Any

from pydantic import ValidationError

from .models import DocgenConfig
from .utils.exceptions import ErrorMessages
from .utils.file_utils import safe_read_yaml
from .utils.logger import get_logger

logger = get_logger("config_manager")


def _configure_logging_level(debug_enabled: bool) -> None:
    """デバッグ設定に基づいてログレベルを設定"""
    level = logging.DEBUG if debug_enabled else logging.INFO

    # 特定のロガーのレベルを設定
    loggers_to_configure = [
        "docgen",
        "config_manager",
        "llm_client",
        "agentsgenerator",
        "readmegenerator",
    ]
    for logger_name in loggers_to_configure:
        logging.getLogger(logger_name).setLevel(level)

    # 全てのハンドラーのレベルも設定
    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.setLevel(level)


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
        """設定ファイルを読み込む"""
        logger.info(f"Loading config from: {self.config_path}")
        if self.config_path.exists():
            logger.info("Config file exists, reading...")
            config = safe_read_yaml(self.config_path)
            if config is not None:
                logger.info("Config loaded successfully")
                # デバッグ設定に基づいてログレベルを設定
                debug_enabled = config.get("debug", {}).get("enabled", False)
                _configure_logging_level(debug_enabled)
                logger.debug(f"Debug mode: {debug_enabled}")
                return config
            else:
                logger.warning(ErrorMessages.CONFIG_LOAD_FAILED)
                logger.info("デフォルト設定を使用します。")
                return self._get_default_config()
        else:
            logger.info("Config file does not exist, creating default")
            return self._create_default_config()

    def _create_default_config(self) -> dict[str, Any]:
        """デフォルト設定を作成して返す"""
        sample_path = self.docgen_dir / "config.yaml.sample"
        if sample_path.exists():
            if self._copy_sample_config(sample_path):
                config = safe_read_yaml(self.config_path)
                return config if config is not None else self._get_default_config()

        logger.warning(ErrorMessages.CONFIG_NOT_FOUND.format(path=self.config_path))
        logger.info("デフォルト設定を使用します。")
        return self._get_default_config()

    def _copy_sample_config(self, sample_path: Path) -> bool:
        """サンプル設定ファイルをコピー"""
        try:
            shutil.copy2(sample_path, self.config_path)
            logger.info(f"{sample_path.name}から{self.config_path.name}を作成しました。")
            return True
        except OSError as e:
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
                "llm_mode": "api",
                "generation": {
                    "agents_mode": "template",
                    "readme_mode": "template",
                    "enable_commit_message": True,
                },
            },
            "exclude": {
                "directories": [],
                "patterns": [],
            },
            "cache": {
                "enabled": True,
            },
            "debug": {
                "enabled": False,
            },
        }

    def get_config(self) -> dict[str, Any]:
        """現在の設定を取得"""
        return self.config

    def _validate_config(self) -> None:
        """
        設定の妥当性を検証

        Raises:
            ValueError: 設定が無効な場合
        """
        try:
            # Pydanticでバリデーション
            validated_config = DocgenConfig(**self.config)
            # バリデーション済みの設定をdictに戻す
            self.config = validated_config.model_dump()
            # デバッグ設定に基づいてログレベルを設定
            debug_enabled = self.config.get("debug", {}).get("enabled", False)
            _configure_logging_level(debug_enabled)
        except ValidationError as e:
            print("設定ファイルにエラーがあります。以下の問題を修正してください:")
            for error in e.errors():
                field_path = ".".join(str(loc) for loc in error["loc"])
                message = error["msg"]
                print(f"  - {field_path}: {message}")
            print("デフォルト設定を使用します。")
            logger.warning(f"設定のバリデーションエラー: {e}")
            logger.info("デフォルト設定を使用します。")
            # デフォルト設定を使用
            default_config = DocgenConfig()
            self.config = default_config.model_dump()

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

    # -------------------------------------------------------------------------
    # Detector Configuration Loading (Merged from ConfigLoader)
    # -------------------------------------------------------------------------

    def load_detector_defaults(self) -> dict[str, Any]:
        """
        Detectorのデフォルト設定を読み込み

        Returns:
            言語名をキーとした設定の辞書
        """
        from .detectors.detector_patterns import DetectorPatterns
        from .models.detector import LanguageConfig, PackageManagerRule

        configs = {}
        for lang, extensions in DetectorPatterns.SOURCE_EXTENSIONS.items():
            pm_rules = []
            # パターンからルールを生成
            if lang in DetectorPatterns.PACKAGE_MANAGER_PATTERNS:
                for patterns, manager in DetectorPatterns.PACKAGE_MANAGER_PATTERNS[lang]:
                    files = patterns if isinstance(patterns, tuple) else (patterns,)
                    pm_rules.append(PackageManagerRule(files=files, manager=manager))

            configs[lang] = LanguageConfig(
                name=lang,
                extensions=tuple(extensions),
                package_files=tuple(DetectorPatterns.get_package_files(lang)),
                package_manager_rules=tuple(pm_rules),
            )
        return configs

    def load_detector_user_overrides(self) -> dict[str, Any]:
        """
        Load detector configuration from config.toml.

        Returns:
            Detector configuration dictionary.
        """
        config_path = self.project_root / "config.toml"
        if not config_path.exists():
            return {}

        try:
            import importlib.util

            if importlib.util.find_spec("tomllib") is not None:
                import tomllib

                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
            else:
                import tomli

                with open(config_path, "rb") as f:
                    config = tomli.load(f)
            return config.get("detectors", {})
        except Exception:
            return {}

    def merge_detector_configs(
        self, defaults: dict[str, Any], overrides: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Detectorのデフォルト設定とユーザー設定をマージ

        Args:
            defaults: デフォルト設定
            overrides: ユーザー設定

        Returns:
            マージされた設定
        """
        merged = dict(defaults)

        for lang_name, override_config in overrides.items():
            if lang_name in merged:
                # 既存の言語設定をマージ
                default_config = merged[lang_name]
                merged[lang_name] = self._merge_language_config(default_config, override_config)
            else:
                # 新しい言語設定を追加
                merged[lang_name] = override_config
                logger.info(f"Added new language config: {lang_name}")

        return merged

    def _merge_language_config(self, default: Any, override: Any) -> Any:
        """
        2つの言語設定をマージ
        """
        from .models.detector import LanguageConfig

        # 拡張子とパッケージファイルは配列を結合
        merged_extensions = tuple(set(default.extensions + override.extensions))
        merged_package_files = tuple(set(default.package_files + override.package_files))

        # パッケージマネージャルールは優先度順にマージ
        merged_rules = tuple(default.package_manager_rules + override.package_manager_rules)

        return LanguageConfig(
            name=default.name,
            extensions=merged_extensions,
            package_files=merged_package_files,
            package_manager_rules=merged_rules,
            custom_detector=override.custom_detector or default.custom_detector,
            custom_package_manager_detector=override.custom_package_manager_detector
            or default.custom_package_manager_detector,
        )

    def _load_toml_config(self, path: Path) -> Any:
        """TOMLファイルから設定を読み込み"""
        import tomllib

        from .models.detector import LanguageConfig, PackageManagerRule

        with open(path, "rb") as f:
            data = tomllib.load(f)

        configs = {}
        if "languages" in data:
            for name, lang_data in data["languages"].items():
                # パッケージマネージャルールの構築
                pm_rules = []
                if "package_managers" in lang_data:
                    for rule in lang_data["package_managers"]:
                        pm_rules.append(
                            PackageManagerRule(
                                files=tuple(rule["files"]),
                                manager=rule["manager"],
                                priority=rule.get("priority", 5),
                                needs_content_check=rule.get("needs_content_check", False),
                            )
                        )

                configs[name] = LanguageConfig(
                    name=name,
                    extensions=tuple(lang_data.get("extensions", [])),
                    package_files=tuple(lang_data.get("package_files", [])),
                    package_manager_rules=tuple(pm_rules),
                )

        return configs

    def _load_user_detector_config(self, path: Path) -> dict[str, Any]:
        """ユーザー設定ファイルを読み込み"""
        import tomllib

        from .models.detector import LanguageConfig, PackageManagerRule

        with open(path, "rb") as f:
            data = tomllib.load(f)

        configs = {}
        if "languages" in data:
            for name, lang_data in data["languages"].items():
                # パッケージマネージャルールの構築
                pm_rules = []
                if "package_managers" in lang_data:
                    for rule in lang_data["package_managers"]:
                        pm_rules.append(
                            PackageManagerRule(
                                files=tuple(rule["files"]),
                                manager=rule["manager"],
                                priority=rule.get("priority", 5),
                                needs_content_check=rule.get("needs_content_check", False),
                            )
                        )

                configs[name] = LanguageConfig(
                    name=name,
                    extensions=tuple(lang_data.get("extensions", [])),
                    package_files=tuple(lang_data.get("package_files", [])),
                    package_manager_rules=tuple(pm_rules),
                )

        return configs
