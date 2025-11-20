"""
エラーハンドリングモジュール
"""

try:
    from .utils.logger import get_logger
except ImportError:
    from utils.logger import get_logger

logger = get_logger("errors")


class DocGenError(Exception):
    """DocGenの基本例外クラス"""

    pass


class ConfigError(DocGenError):
    """設定関連のエラー"""

    pass


class LanguageDetectionError(DocGenError):
    """言語検出関連のエラー"""

    pass


class DocumentGenerationError(DocGenError):
    """ドキュメント生成関連のエラー"""

    pass


def handle_error(error: Exception, context: str = "", raise_exception: bool = False) -> None:
    """
    エラーを統一的に処理

    Args:
        error: 発生した例外
        context: エラーのコンテキスト情報
        raise_exception: DocGenErrorを発生させるかどうか
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)

    if raise_exception:
        if isinstance(error, DocGenError):
            raise error
        else:
            raise DocGenError(error_msg) from error
