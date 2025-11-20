"""
カスタム例外クラス
ドキュメント生成システムで使用する例外を定義
"""


class DocGenError(Exception):
    """ドキュメント生成システムの基本例外クラス"""

    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class ConfigError(DocGenError):
    """設定関連のエラー"""

    pass


class LLMError(DocGenError):
    """LLM関連のエラー"""

    pass


class ParseError(DocGenError):
    """解析関連のエラー"""

    pass


class CacheError(DocGenError):
    """キャッシュ関連のエラー"""

    pass


class FileOperationError(DocGenError):
    """ファイル操作関連のエラー"""

    pass
