"""
ConfigLoaderのテスト
"""

from pathlib import Path
import tempfile

import pytest

from docgen.detectors.config_loader import ConfigLoader
from docgen.detectors.detector_config import LanguageConfig, PackageManagerRule


class TestConfigLoader:
    """ConfigLoaderクラスのテスト"""

    def test_load_defaults(self):
        """デフォルト設定の読み込みテスト"""
        loader = ConfigLoader(Path.cwd())
        configs = loader.load_defaults()

        # 少なくとも主要な言語が含まれていること
        assert "python" in configs
        assert "javascript" in configs
        assert "go" in configs

        # Python設定の検証
        python_config = configs["python"]
        assert python_config.name == "python"
        assert ".py" in python_config.extensions
        assert "requirements.txt" in python_config.package_files
        assert len(python_config.package_manager_rules) > 0

    def test_load_user_overrides_nonexistent(self):
        """存在しないユーザー設定の読み込みテスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = ConfigLoader(Path(tmpdir))
            configs = loader.load_user_overrides()
            assert configs == {}

    def test_load_user_overrides(self):
        """ユーザー設定の読み込みテスト"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            agent_dir = tmppath / ".agent"
            agent_dir.mkdir()

            # ユーザー設定を作成
            user_config = agent_dir / "detectors.toml"
            user_config.write_text(
                """
[languages.elixir]
extensions = [".ex", ".exs"]
package_files = ["mix.exs", "mix.lock"]

[[languages.elixir.package_managers]]
files = ["mix.lock"]
manager = "mix"
priority = 10
"""
            )

            loader = ConfigLoader(tmppath)
            configs = loader.load_user_overrides()

            assert "elixir" in configs
            elixir_config = configs["elixir"]
            assert elixir_config.name == "elixir"
            assert ".ex" in elixir_config.extensions
            assert "mix.exs" in elixir_config.package_files

    def test_merge_configs_new_language(self):
        """新しい言語の追加マージテスト"""
        loader = ConfigLoader(Path.cwd())

        defaults = {
            "python": LanguageConfig(
                name="python", extensions=(".py",), package_files=("requirements.txt",)
            )
        }

        overrides = {
            "elixir": LanguageConfig(name="elixir", extensions=(".ex",), package_files=("mix.exs",))
        }

        merged = loader.merge_configs(defaults, overrides)

        assert "python" in merged
        assert "elixir" in merged

    def test_merge_configs_existing_language(self):
        """既存言語の設定マージテスト"""
        loader = ConfigLoader(Path.cwd())

        defaults = {
            "python": LanguageConfig(
                name="python",
                extensions=(".py",),
                package_files=("requirements.txt",),
                package_manager_rules=(
                    PackageManagerRule(files=("requirements.txt",), manager="pip"),
                ),
            )
        }

        overrides = {
            "python": LanguageConfig(
                name="python",
                extensions=(".pyx",),
                package_files=("setup.py",),
                package_manager_rules=(
                    PackageManagerRule(files=("uv.lock",), manager="uv", priority=10),
                ),
            )
        }

        merged = loader.merge_configs(defaults, overrides)

        python_config = merged["python"]
        # 拡張子がマージされている
        assert ".py" in python_config.extensions
        assert ".pyx" in python_config.extensions

        # パッケージファイルがマージされている
        assert "requirements.txt" in python_config.package_files
        assert "setup.py" in python_config.package_files

        # パッケージマネージャルールがマージされている
        assert len(python_config.package_manager_rules) == 2

    def test_package_manager_rule_validation(self):
        """PackageManagerRuleのバリデーションテスト"""
        # 正常なルール
        rule = PackageManagerRule(files=("test.lock",), manager="test")
        assert rule.files == ("test.lock",)
        assert rule.manager == "test"

        # filesが空の場合エラー
        with pytest.raises(ValueError):
            PackageManagerRule(files=(), manager="test")

        # managerが空の場合エラー
        with pytest.raises(ValueError):
            PackageManagerRule(files=("test.lock",), manager="")

    def test_language_config_validation(self):
        """LanguageConfigのバリデーションテスト"""
        # 正常な設定
        config = LanguageConfig(name="test")
        assert config.name == "test"

        # nameが空の場合エラー
        with pytest.raises(ValueError):
            LanguageConfig(name="")

    def test_sorted_package_manager_rules(self):
        """パッケージマネージャルールのソートテスト"""
        config = LanguageConfig(
            name="test",
            package_manager_rules=(
                PackageManagerRule(files=("a.lock",), manager="a", priority=5),
                PackageManagerRule(files=("b.lock",), manager="b", priority=10),
                PackageManagerRule(files=("c.lock",), manager="c", priority=7),
            ),
        )

        sorted_rules = config.get_sorted_package_manager_rules()
        assert len(sorted_rules) == 3
        assert sorted_rules[0].manager == "b"  # priority 10
        assert sorted_rules[1].manager == "c"  # priority 7
        assert sorted_rules[2].manager == "a"  # priority 5
