"""
プロンプトローダーモジュール
YAMLファイルからプロンプトを読み込み、キャッシュする
"""

from pathlib import Path
from typing import Any

import yaml

from .logger import get_logger


class PromptLoader:
    """プロンプトをYAMLファイルから読み込むクラス"""

    _cache: dict[str, dict[str, Any]] = {}
    _logger = get_logger("prompt_loader")

    @classmethod
    def _get_prompts_dir(cls) -> Path:
        """プロンプトディレクトリのパスを取得"""
        # docgen/utils/prompt_loader.py から docgen/prompts/ へのパス
        return Path(__file__).parent.parent / "prompts"

    @classmethod
    def _load_yaml_file(cls, file_name: str) -> dict[str, Any]:
        """
        YAMLファイルを読み込む（キャッシュ付き）

        Args:
            file_name: YAMLファイル名（例: 'agents_prompts.yaml'）

        Returns:
            YAMLファイルの内容

        Raises:
            FileNotFoundError: ファイルが見つからない場合
            yaml.YAMLError: YAML解析エラーの場合
        """
        if file_name in cls._cache:
            return cls._cache[file_name]

        prompts_dir = cls._get_prompts_dir()
        file_path = prompts_dir / file_name

        if not file_path.exists():
            cls._logger.error(f"プロンプトファイルが見つかりません: {file_path}")
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        try:
            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                cls._cache[file_name] = data
                cls._logger.debug(f"プロンプトファイルを読み込みました: {file_name}")
                return data
        except yaml.YAMLError as e:
            cls._logger.error(f"YAML解析エラー: {file_name}, {e}")
            raise

    @classmethod
    def load_prompt(cls, file_name: str, key: str, **kwargs) -> str:
        """
        プロンプトを読み込む

        Args:
            file_name: YAMLファイル名（例: 'agents_prompts.yaml'）
            key: プロンプトのキー（例: 'overview', 'full'）
            **kwargs: テンプレート変数の置換用パラメータ

        Returns:
            読み込んだプロンプト文字列（テンプレート変数が置換済み）

        Raises:
            FileNotFoundError: ファイルが見つからない場合
            KeyError: 指定されたキーが見つからない場合
        """
        data = cls._load_yaml_file(file_name)

        if "prompts" not in data:
            cls._logger.error(f"'prompts'キーが見つかりません: {file_name}")
            raise KeyError(f"'prompts' key not found in {file_name}")

        if key not in data["prompts"]:
            cls._logger.error(f"プロンプトキーが見つかりません: {key} in {file_name}")
            raise KeyError(f"Prompt key '{key}' not found in {file_name}")

        prompt = data["prompts"][key]

        # テンプレート変数を置換
        if kwargs:
            prompt = prompt.format(**kwargs)

        return prompt

    @classmethod
    def load_system_prompt(cls, file_name: str, key: str, **kwargs) -> str:
        """
        システムプロンプトを読み込む

        Args:
            file_name: YAMLファイル名（例: 'agents_prompts.yaml'）
            key: システムプロンプトのキー（例: 'overview', 'generate'）
            **kwargs: テンプレート変数の置換用パラメータ

        Returns:
            読み込んだシステムプロンプト文字列（テンプレート変数が置換済み）

        Raises:
            FileNotFoundError: ファイルが見つかりません場合
            KeyError: 指定されたキーが見つからない場合
        """
        data = cls._load_yaml_file(file_name)

        if "system_prompts" not in data:
            cls._logger.error(f"'system_prompts'キーが見つかりません: {file_name}")
            raise KeyError(f"'system_prompts' key not found in {file_name}")

        if key not in data["system_prompts"]:
            cls._logger.error(f"システムプロンプトキーが見つかりません: {key} in {file_name}")
            raise KeyError(f"System prompt key '{key}' not found in {file_name}")

        system_prompt = data["system_prompts"][key]

        # テンプレート変数を置換
        if kwargs:
            system_prompt = system_prompt.format(**kwargs)

        return system_prompt

    @classmethod
    def clear_cache(cls):
        """キャッシュをクリア（主にテスト用）"""
        cls._cache.clear()
        cls._logger.debug("プロンプトキャッシュをクリアしました")
