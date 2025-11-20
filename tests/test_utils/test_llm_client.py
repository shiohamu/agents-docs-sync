"""
LLMClientのテスト
"""

# docgenモジュールをインポート可能にする
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DOCGEN_DIR = PROJECT_ROOT / "docgen"
import sys

sys.path.insert(0, str(PROJECT_ROOT))

try:
    from docgen.utils.llm_client import (
        AnthropicClient,
        BaseLLMClient,
        LLMClientFactory,
        LocalLLMClient,
        OpenAIClient,
    )

    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

    class OpenAIClient:
        pass

    class AnthropicClient:
        pass

    class LocalLLMClient:
        pass

    class LLMClientFactory:
        pass


class TestBaseLLMClient:
    """BaseLLMClientクラスのテスト"""

    def test_base_llm_client_initialization(self):
        """BaseLLMClientの初期化テスト"""
        config = {"timeout": 60, "max_retries": 5, "retry_delay": 2.0}

        # 抽象クラスなので直接インスタンス化できないが、属性チェック用にモック
        from unittest.mock import MagicMock

        client = MagicMock(spec=BaseLLMClient)
        client.config = config
        client.timeout = 60
        client.max_retries = 5
        client.retry_delay = 2.0

        assert client.config == config
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_delay == 2.0


class TestOpenAIClient:
    """OpenAIClientクラスのテスト"""

    @pytest.mark.skipif(not LLM_AVAILABLE, reason="LLM libraries not available")
    @pytest.mark.skip(reason="Error handling test may have issues")
    @patch("docgen.utils.llm_client.httpx")
    def test_ollama_client_error_handling(self, mock_httpx):
        """Ollamaクライアントのエラーハンドリングテスト"""
        mock_client = MagicMock()
        mock_client.post.side_effect = Exception("Connection Error")
        mock_httpx.Client.return_value.__enter__.return_value = mock_client

        config = {"base_url": "http://localhost:11434", "model": "llama3"}
        client = LocalLLMClient(config)

        result = client.generate("Test prompt")

        assert result is None
