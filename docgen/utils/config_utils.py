"""
設定アクセスユーティリティ
"""

from typing import Any


def get_nested_config(config: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    ネストされた設定値を安全に取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        設定値。存在しない場合はdefault

    Examples:
        >>> config = {"a": {"b": {"c": "value"}}}
        >>> get_nested_config(config, "a", "b", "c")
        'value'
        >>> get_nested_config(config, "a", "x", "y", default="default")
        'default'
    """
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def get_config_bool(config: dict[str, Any], *keys: str, default: bool = False) -> bool:
    """
    設定値をブール値として取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        ブール値
    """
    value = get_nested_config(config, *keys, default=default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


def get_config_list(config: dict[str, Any], *keys: str, default: list | None = None) -> list:
    """
    設定値をリストとして取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        リスト
    """
    if default is None:
        default = []
    value = get_nested_config(config, *keys, default=default)
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # カンマ区切りをサポート
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, (int, float)):
        return [value]
    return default


def get_config_str(config: dict[str, Any], *keys: str, default: str = "") -> str:
    """
    設定値を文字列として取得

    Args:
        config: 設定辞書
        *keys: 取得するキーのパス
        default: デフォルト値

    Returns:
        文字列
    """
    value = get_nested_config(config, *keys, default=default)
    if value is None:
        return default
    if isinstance(value, str):
        return value
    return str(value)


def get_message(
    config: dict[str, Any] | None, message_key: str, language: str | None = None
) -> str:
    """
    多言語対応メッセージを取得

    Args:
        config: 設定辞書（Noneの場合はデフォルト値を使用）
        message_key: メッセージキー（例: "default_description"）
        language: 言語コード（Noneの場合は設定から取得、それもなければ"en"）

    Returns:
        メッセージ文字列
    """
    # デフォルトメッセージ（英語）
    default_messages: dict[str, dict[str, str]] = {
        "default_description": {
            "en": "Please describe this project here.",
            "ja": "このプロジェクトの説明をここに記述してください。",
            "ko": "여기에 프로젝트 설명을 작성하세요.",
        }
    }

    # 言語を決定
    if language is None:
        if config:
            language = config.get("general", {}).get("default_language", "en")
        else:
            language = "en"

    # 設定からメッセージを取得
    if config:
        messages = config.get("messages", {})
        message_dict = messages.get(message_key, {})
        if isinstance(message_dict, dict) and language in message_dict:
            return message_dict[language]

    # デフォルトメッセージから取得
    if message_key in default_messages:
        return default_messages[message_key].get(language, default_messages[message_key]["en"])

    # フォールバック
    return ""
