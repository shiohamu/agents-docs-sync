"""
検出設定ファイルのローダー
"""

from pathlib import Path
import sys

# Python 3.11+ uses tomllib, earlier versions use tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

from ..utils.logger import get_logger
from .detector_config import LanguageConfig, PackageManagerRule

logger = get_logger("config_loader")


class ConfigLoader:
    """検出設定ローダー"""

    def __init__(self, project_root: Path):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
        """
        self.project_root = project_root
        self._config_cache: dict[str, LanguageConfig] = {}

    def load_defaults(self) -> dict[str, LanguageConfig]:
        """
        デフォルト設定を読み込み

        Returns:
            言語名をキーとした設定の辞書
        """
        if tomllib is None:
            logger.warning("TOML parser not available, skipping config loading")
            return {}

        configs_dir = Path(__file__).parent / "configs"
        if not configs_dir.exists():
            logger.warning(f"Configs directory not found: {configs_dir}")
            return {}

        configs = {}
        for toml_file in configs_dir.glob("*.toml"):
            try:
                config = self._load_toml_config(toml_file)
                configs[config.name] = config
                logger.debug(f"Loaded config: {config.name}")
            except Exception as e:
                logger.warning(f"Failed to load config file {toml_file}: {e}")

        return configs

    def load_user_overrides(self) -> dict[str, LanguageConfig]:
        """
        ユーザー設定のオーバーライドを読み込み

        Returns:
            言語名をキーとした設定の辞書
        """
        if tomllib is None:
            return {}

        user_config_path = self.project_root / ".agent" / "detectors.toml"
        if not user_config_path.exists():
            logger.debug("No user config found")
            return {}

        try:
            return self._load_user_config(user_config_path)
        except Exception as e:
            logger.warning(f"Failed to load user config: {e}")
            return {}

    def merge_configs(
        self, defaults: dict[str, LanguageConfig], overrides: dict[str, LanguageConfig]
    ) -> dict[str, LanguageConfig]:
        """
        デフォルト設定とユーザー設定をマージ

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

    def _merge_language_config(
        self, default: LanguageConfig, override: LanguageConfig
    ) -> LanguageConfig:
        """
        2つの言語設定をマージ

        Args:
            default: デフォルト設定
            override: オーバーライド設定

        Returns:
            マージされた設定
        """
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

    def _load_toml_config(self, path: Path) -> LanguageConfig:
        """
        TOMLファイルから設定を読み込み

        Args:
            path: TOMLファイルのパス

        Returns:
            言語設定
        """
        with open(path, "rb") as f:
            data = tomllib.load(f)

        # 基本情報
        lang_info = data.get("language", {})
        name = lang_info.get("name")
        if not name:
            raise ValueError(f"Language name not found in {path}")

        extensions = tuple(lang_info.get("extensions", []))

        # 検出設定
        detection = data.get("detection", {})
        package_files = tuple(detection.get("package_files", []))

        # パッケージマネージャルール
        pm_rules = []
        for rule_data in data.get("package_managers", []):
            files = rule_data.get("files", [])
            if isinstance(files, str):
                files = [files]

            rule = PackageManagerRule(
                files=tuple(files),
                manager=rule_data.get("manager", ""),
                priority=rule_data.get("priority", 5),
                needs_content_check=rule_data.get("needs_content_check", False),
            )
            pm_rules.append(rule)

        return LanguageConfig(
            name=name,
            extensions=extensions,
            package_files=package_files,
            package_manager_rules=tuple(pm_rules),
        )

    def _load_user_config(self, path: Path) -> dict[str, LanguageConfig]:
        """
        ユーザー設定ファイルを読み込み

        Args:
            path: ユーザー設定ファイルのパス

        Returns:
            言語名をキーとした設定の辞書
        """
        with open(path, "rb") as f:
            data = tomllib.load(f)

        configs = {}
        languages = data.get("languages", {})

        for lang_name, lang_data in languages.items():
            # 拡張子
            extensions = tuple(lang_data.get("extensions", []))

            # パッケージファイル
            package_files = tuple(lang_data.get("package_files", []))

            # パッケージマネージャルール
            pm_rules = []
            for rule_data in lang_data.get("package_managers", []):
                files = rule_data.get("files", [])
                if isinstance(files, str):
                    files = [files]

                rule = PackageManagerRule(
                    files=tuple(files),
                    manager=rule_data.get("manager", ""),
                    priority=rule_data.get("priority", 5),
                    needs_content_check=rule_data.get("needs_content_check", False),
                )
                pm_rules.append(rule)

            configs[lang_name] = LanguageConfig(
                name=lang_name,
                extensions=extensions,
                package_files=package_files,
                package_manager_rules=tuple(pm_rules),
            )

        return configs
