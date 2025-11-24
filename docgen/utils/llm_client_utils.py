"""Common utilities for LLM client initialization and error handling."""

import os
from typing import Any

from ..utils.exceptions import ConfigError, ErrorMessages
from ..utils.logger import get_logger

logger = get_logger("llm_client_utils")

# Default LLM models
DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "anthropic": "claude-3-5-sonnet-20241022",
    "ollama": "llama3",
    "lmstudio": "llama3",
}


class LLMClientInitializer:
    """Common initialization patterns for LLM clients."""

    @staticmethod
    def setup_provider_config(config: dict[str, Any], provider: str) -> dict[str, Any]:
        """
        Set up provider-specific configuration.

        Args:
            config: Configuration dictionary
            provider: Provider name ('openai', 'anthropic', etc.)

        Returns:
            Updated configuration dictionary
        """
        if isinstance(config, dict):
            config = config.copy()
            config["provider"] = provider
        return config

    @staticmethod
    def get_api_key(config, env_var: str, default_env: str) -> str:
        """
        Get API key from config or environment.

        Args:
            config: LLMConfig object
            env_var: Environment variable name from config
            default_env: Default environment variable name

        Returns:
            API key string
        """
        env_name = getattr(config, "api_key_env", None) or default_env
        api_key = getattr(config, "api_key", None) or os.getenv(env_name, "")
        return api_key

    @staticmethod
    def initialize_client_with_fallback(
        client_class, config: dict[str, Any], import_name: str, package_name: str, error_prefix: str
    ):
        """
        Initialize LLM client with common error handling.

        Args:
            client_class: Client class to instantiate
            config: Configuration dictionary
            import_name: Module name to import
            package_name: Package name for error messages
            error_prefix: Prefix for error messages

        Returns:
            Initialized client instance

        Raises:
            ImportError: If required package is not installed
            ConfigError: If initialization fails
        """
        try:
            # Import the module
            module = __import__(import_name)

            # Create client instance
            return client_class(config)

        except ImportError:
            raise ImportError(
                f"{package_name}パッケージが必要です。`pip install {package_name}`でインストールしてください。"
            ) from None
        except Exception as e:
            raise ConfigError(
                ErrorMessages.CLIENT_INIT_FAILED.format(prefix=error_prefix, error=e)
            ) from e

    @staticmethod
    def handle_api_response(response, response_processor=None):
        """
        Handle API response with common error checking.

        Args:
            response: API response object
            response_processor: Optional function to process response content

        Returns:
            Processed response content or None
        """
        if not response:
            return None

        try:
            if response_processor:
                return response_processor(response)
            else:
                # Default processing - try common response formats
                if hasattr(response, "choices") and response.choices:
                    # OpenAI-style response
                    choice = response.choices[0]
                    if hasattr(choice, "message") and hasattr(choice.message, "content"):
                        return choice.message.content.strip()
                    elif hasattr(choice, "text"):
                        return choice.text.strip()

                elif hasattr(response, "content"):
                    # Anthropic-style response
                    if isinstance(response.content, list):
                        text_content = ""
                        for block in response.content:
                            if hasattr(block, "text") and block.text:
                                text_content += block.text
                        return text_content.strip() if text_content else None
                    else:
                        return str(response.content).strip()

                return None

        except Exception as e:
            logger.error(f"APIレスポンス処理エラー: {e}")
            return None

    @staticmethod
    def create_retry_wrapper(max_retries: int, retry_delay: float):
        """
        Create a retry wrapper function.

        Args:
            max_retries: Maximum number of retries
            retry_delay: Delay between retries

        Returns:
            Retry wrapper function
        """

        def retry_with_backoff(func, *args, **kwargs):
            """Execute function with retry logic."""
            import time

            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (2**attempt))  # Exponential backoff
                    else:
                        logger.error(f"リトライ上限に達しました: {e}")
                        break
            return None

        return retry_with_backoff
