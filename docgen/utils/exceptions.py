"""
カスタム例外クラス
ドキュメント生成システムで使用する例外を定義
"""

from typing import Any


class DocGenError(Exception):
    """ドキュメント生成システムの基本例外クラス"""

    def __init__(
        self,
        message: str,
        details: str | None = None,
        error_code: str | None = None,
        context: dict[str, Any] | None = None,
    ):
        self.message = message
        self.details = details
        self.error_code = error_code
        self.context = context

    def __str__(self) -> str:
        result = self.message
        if self.details:
            result += f": {self.details}"
        # エラーコードはデバッグ時のみ表示
        # if self.error_code:
        #     result += f" (code: {self.error_code})"
        return result


class ConfigError(DocGenError):
    """設定関連のエラー"""

    def __init__(self, message: str, config_path: str | None = None, **kwargs):
        # 第2引数をdetailsとして扱う（後方互換性のため）
        details = kwargs.get("details") or config_path
        super().__init__(
            message=message,
            details=details,
            error_code="CONFIG_ERROR",
            context={"config_path": config_path} if config_path else None,
            **kwargs,
        )


class LLMError(DocGenError):
    """LLM関連のエラー"""

    def __init__(
        self, message: str, provider: str | None = None, model: str | None = None, **kwargs
    ):
        # 第2引数をdetailsとして扱う（後方互換性のため）
        details = kwargs.get("details") or provider
        super().__init__(
            message=message,
            details=details,
            error_code="LLM_ERROR",
            context={"provider": provider, "model": model} if provider or model else None,
            **kwargs,
        )


class ParseError(DocGenError):
    """解析関連のエラー"""

    def __init__(
        self, message: str, file_path: str | None = None, language: str | None = None, **kwargs
    ):
        # 第2引数をdetailsとして扱う（後方互換性のため）
        details = kwargs.get("details") or file_path
        super().__init__(
            message=message,
            details=details,
            error_code="PARSE_ERROR",
            context={"file_path": file_path, "language": language}
            if file_path or language
            else None,
            **kwargs,
        )


class CacheError(DocGenError):
    """キャッシュ関連のエラー"""

    def __init__(self, message: str, cache_key: str | None = None, **kwargs):
        # 第2引数をdetailsとして扱う（後方互換性のため）
        details = kwargs.get("details") or cache_key
        super().__init__(
            message=message,
            details=details,
            error_code="CACHE_ERROR",
            context={"cache_key": cache_key} if cache_key else None,
            **kwargs,
        )


class FileOperationError(DocGenError):
    """ファイル操作関連のエラー"""

    def __init__(
        self, message: str, file_path: str | None = None, operation: str | None = None, **kwargs
    ):
        # 第2引数をdetailsとして扱う（後方互換性のため）
        details = kwargs.get("details") or file_path
        super().__init__(
            message=message,
            details=details,
            error_code="FILE_ERROR",
            context={"file_path": file_path, "operation": operation}
            if file_path or operation
            else None,
            **kwargs,
        )
