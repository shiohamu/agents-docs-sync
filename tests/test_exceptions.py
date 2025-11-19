"""
カスタム例外クラスのテスト
"""

import pytest
from utils.exceptions import (
    DocGenError,
    ConfigError,
    LLMError,
    ParseError,
    CacheError,
    FileOperationError,
)


class TestDocGenError:
    """DocGenErrorクラスのテスト"""

    def test_init_with_message_only(self):
        """メッセージのみで初期化"""
        error = DocGenError("Test message")
        assert error.message == "Test message"
        assert error.details is None
        assert str(error) == "Test message"

    def test_init_with_message_and_details(self):
        """メッセージと詳細で初期化"""
        error = DocGenError("Test message", "Additional details")
        assert error.message == "Test message"
        assert error.details == "Additional details"
        assert str(error) == "Test message: Additional details"

    def test_str_with_details(self):
        """__str__メソッドのテスト（詳細あり）"""
        error = DocGenError("Error occurred", "File not found")
        assert str(error) == "Error occurred: File not found"

    def test_str_without_details(self):
        """__str__メソッドのテスト（詳細なし）"""
        error = DocGenError("Simple error")
        assert str(error) == "Simple error"

    def test_inheritance_from_exception(self):
        """Exceptionからの継承確認"""
        error = DocGenError("Test")
        assert isinstance(error, Exception)


class TestConfigError:
    """ConfigErrorクラスのテスト"""

    def test_inheritance(self):
        """DocGenErrorからの継承確認"""
        error = ConfigError("Config error")
        assert isinstance(error, DocGenError)
        assert isinstance(error, Exception)

    def test_message_preservation(self):
        """メッセージの保持確認"""
        error = ConfigError("Invalid config", "Missing required field")
        assert error.message == "Invalid config"
        assert error.details == "Missing required field"
        assert str(error) == "Invalid config: Missing required field"


class TestLLMError:
    """LLMErrorクラスのテスト"""

    def test_inheritance(self):
        """DocGenErrorからの継承確認"""
        error = LLMError("LLM error")
        assert isinstance(error, DocGenError)
        assert isinstance(error, Exception)

    def test_simple_message(self):
        """シンプルなメッセージテスト"""
        error = LLMError("API timeout")
        assert str(error) == "API timeout"


class TestParseError:
    """ParseErrorクラスのテスト"""

    def test_inheritance(self):
        """DocGenErrorからの継承確認"""
        error = ParseError("Parse error")
        assert isinstance(error, DocGenError)
        assert isinstance(error, Exception)

    def test_with_details(self):
        """詳細付きエラーテスト"""
        error = ParseError("Syntax error", "Unexpected token")
        assert str(error) == "Syntax error: Unexpected token"


class TestCacheError:
    """CacheErrorクラスのテスト"""

    def test_inheritance(self):
        """DocGenErrorからの継承確認"""
        error = CacheError("Cache error")
        assert isinstance(error, DocGenError)
        assert isinstance(error, Exception)

    def test_message_only(self):
        """メッセージのみのテスト"""
        error = CacheError("Cache write failed")
        assert str(error) == "Cache write failed"


class TestFileOperationError:
    """FileOperationErrorクラスのテスト"""

    def test_inheritance(self):
        """DocGenErrorからの継承確認"""
        error = FileOperationError("File operation error")
        assert isinstance(error, DocGenError)
        assert isinstance(error, Exception)

    def test_with_details(self):
        """詳細付きエラーテスト"""
        error = FileOperationError("Permission denied", "/path/to/file")
        assert str(error) == "Permission denied: /path/to/file"


class TestExceptionHierarchy:
    """例外クラスの階層テスト"""

    def test_all_exceptions_are_docgen_errors(self):
        """すべての例外がDocGenErrorのサブクラスであることを確認"""
        exceptions = [
            ConfigError("test"),
            LLMError("test"),
            ParseError("test"),
            CacheError("test"),
            FileOperationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, DocGenError)
            assert isinstance(exc, Exception)

    def test_exception_raising(self):
        """例外のraiseとcatchテスト"""
        with pytest.raises(DocGenError):
            raise DocGenError("Test error")

        with pytest.raises(ConfigError):
            raise ConfigError("Config test")

        with pytest.raises(LLMError):
            raise LLMError("LLM test")
