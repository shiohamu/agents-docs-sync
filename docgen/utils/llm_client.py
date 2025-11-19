"""
LLMクライアントモジュール
OpenAI、Anthropic、ローカルLLM（Ollama、LM Studio）に対応
"""

import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from ..utils.logger import get_logger
    from ..utils.exceptions import ConfigError, LLMError
except ImportError:
    import sys

    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from utils.logger import get_logger

    # Fallback for exceptions
    class ConfigError(ValueError):
        pass

    class LLMError(Exception):
        pass


logger = get_logger("llm_client")


class BaseLLMClient(ABC):
    """LLMクライアントの抽象基底クラス"""

    def __init__(self, config: Dict[str, Any]):
        """
        初期化

        Args:
            config: LLM設定辞書
        """
        self.config: Dict[str, Any] = config
        self.timeout: int = config.get("timeout", 30)
        self.max_retries: int = config.get("max_retries", 3)
        self.retry_delay: float = config.get("retry_delay", 1.0)

    @abstractmethod
    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """
        テキストを生成

        Args:
            prompt: プロンプト
            system_prompt: システムプロンプト（オプション）
            **kwargs: その他のパラメータ

        Returns:
            生成されたテキスト（エラー時はNone）
        """
        pass

    def create_outlines_model(self):
        """
        Outlinesモデルを作成

        Returns:
            Outlinesモデルインスタンス（Outlinesが利用できない場合はNone）
        """
        try:
            import outlines

            return self._create_outlines_model_internal(outlines)
        except ImportError:
            logger.warning("Outlinesがインストールされていません")
            return None
        except Exception as e:
            logger.error(f"Outlinesモデルの作成に失敗しました: {e}")
            return None

    @abstractmethod
    def _create_outlines_model_internal(self, outlines):
        """
        Outlinesモデルを作成（内部実装）

        Args:
            outlines: Outlinesモジュール

        Returns:
            Outlinesモデルインスタンス
        """
        pass

    def _retry_with_backoff(self, func, *args, **kwargs):
        """
        リトライ機能付きで関数を実行

        Args:
            func: 実行する関数
            *args: 関数の引数
            **kwargs: 関数のキーワード引数

        Returns:
            関数の戻り値
        """
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    logger.warning(
                        f"LLM呼び出し失敗 (試行 {attempt + 1}/{self.max_retries}): {e}. {delay}秒後にリトライします..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"LLM呼び出しが{self.max_retries}回失敗しました: {e}")
        raise last_exception


class OpenAIClient(BaseLLMClient):
    """OpenAI APIクライアント"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import openai

            self.client: openai.OpenAI = openai.OpenAI(
                api_key=os.getenv(config.get("api_key_env", "OPENAI_API_KEY"), ""),
                base_url=config.get("endpoint"),  # カスタムエンドポイント対応
            )
            self.model: str = config.get("model", "gpt-4o")
        except ImportError:
            raise ImportError(
                "openaiパッケージが必要です。`pip install openai`でインストールしてください。"
            )
        except Exception as e:
            raise ConfigError(f"OpenAIクライアントの初期化に失敗しました: {e}")

    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """OpenAI APIを使用してテキストを生成"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self._retry_with_backoff(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                timeout=self.timeout,
                **kwargs,
            )

            if response and response.choices:
                return response.choices[0].message.content.strip()
            return None
        except Exception as e:
            logger.error(f"OpenAI API呼び出しエラー: {e}")
            return None

    def _create_outlines_model_internal(self, outlines):
        """OpenAI用のOutlinesモデルを作成"""
        return outlines.from_openai(self.client, self.model)

    def _create_outlines_model_internal(self, outlines):
        """OpenAI用のOutlinesモデルを作成"""
        return outlines.from_openai(self.client, self.model)


class AnthropicClient(BaseLLMClient):
    """Anthropic APIクライアント"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import anthropic

            self.client = anthropic.Anthropic(
                api_key=os.getenv(config.get("api_key_env", "ANTHROPIC_API_KEY"), "")
            )
            self.model = config.get("model", "claude-3-5-sonnet-20241022")
        except ImportError:
            raise ImportError(
                "anthropicパッケージが必要です。`pip install anthropic`でインストールしてください。"
            )
        except Exception as e:
            raise ValueError(f"Anthropicクライアントの初期化に失敗しました: {e}")

    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """Anthropic APIを使用してテキストを生成"""
        try:
            messages = [{"role": "user", "content": prompt}]

            api_kwargs = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", 4096),
                "messages": messages,
                "timeout": self.timeout,
            }

            if system_prompt:
                api_kwargs["system"] = system_prompt

            response = self._retry_with_backoff(
                self.client.messages.create, **api_kwargs
            )

            if response and response.content:
                # Anthropicのレスポンス形式に合わせて処理
                text_content = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        text_content += block.text
                return text_content.strip() if text_content else None
            return None
        except Exception as e:
            logger.error(f"Anthropic API呼び出しエラー: {e}")
            return None

    def _create_outlines_model_internal(self, outlines):
        """Anthropic用のOutlinesモデルを作成（現在未対応）"""
        # Outlinesは現在Anthropicを直接サポートしていないため、未実装
        logger.warning("Anthropic用のOutlinesモデルは現在サポートされていません")
        return None

    def _create_outlines_model_internal(self, outlines):
        """Anthropic用のOutlinesモデルを作成（現在未対応）"""
        # Outlinesは現在Anthropicを直接サポートしていないため、未実装
        logger.warning("Anthropic用のOutlinesモデルは現在サポートされていません")
        return None


class LocalLLMClient(BaseLLMClient):
    """ローカルLLMクライアント（Ollama、LM Studio対応）"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import httpx

            self.httpx = httpx
        except ImportError:
            raise ImportError(
                "httpxパッケージが必要です。`pip install httpx`でインストールしてください。"
            )

        self.base_url: str = config.get("base_url", "http://localhost:11434")
        self.model: str = config.get("model", "llama3")
        self.provider: str = config.get("provider", "ollama")

        # ベースURLの正規化（末尾のスラッシュを削除）
        self.base_url = self.base_url.rstrip("/")

    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """ローカルLLMを使用してテキストを生成"""
        try:
            if self.provider == "ollama":
                return self._generate_ollama(prompt, system_prompt, **kwargs)
            elif self.provider in ["lmstudio", "custom"]:
                return self._generate_openai_compatible(prompt, system_prompt, **kwargs)
            else:
                logger.error(f"サポートされていないプロバイダー: {self.provider}")
                return None
        except Exception as e:
            logger.error(f"ローカルLLM呼び出しエラー: {e}")
            return None

    def _create_outlines_model_internal(self, outlines):
        """ローカルLLM用のOutlinesモデルを作成"""
        # OpenAI互換APIとして扱う
        import openai

        openai_client = openai.OpenAI(
            base_url=self.base_url,
            api_key="dummy",  # ローカルでは不要
        )
        return outlines.from_openai(openai_client, self.model)

    def _generate_ollama(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """Ollama APIを使用してテキストを生成"""
        try:
            # OllamaのAPI形式
            url = f"{self.base_url}/api/generate"

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }

            if system_prompt:
                payload["system"] = system_prompt

            response = self._retry_with_backoff(
                lambda: self.httpx.post(url, json=payload, timeout=self.timeout)
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                logger.error(
                    f"Ollama APIエラー: {response.status_code} - {response.text}"
                )
                return None
        except Exception as e:
            logger.error(f"Ollama API呼び出しエラー: {e}")
            return None

    def _generate_openai_compatible(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """OpenAI互換APIを使用してテキストを生成（LM Studio等）"""
        try:
            # OpenAI互換のAPI形式
            url = f"{self.base_url}/v1/chat/completions"

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 4096),
            }

            response = self._retry_with_backoff(
                lambda: self.httpx.post(url, json=payload, timeout=self.timeout)
            )

            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"].strip()
                return None
            else:
                logger.error(
                    f"OpenAI互換APIエラー: {response.status_code} - {response.text}"
                )
                return None
        except Exception as e:
            logger.error(f"OpenAI互換API呼び出しエラー: {e}")
            return None


class LLMClientFactory:
    """LLMクライアントのファクトリークラス"""

    @staticmethod
    def create_client(
        config: Dict[str, Any], mode: str = "api"
    ) -> Optional[BaseLLMClient]:
        """
        LLMクライアントを作成

        Args:
            config: LLM設定辞書
            mode: 'api' または 'local'

        Returns:
            LLMクライアントインスタンス（エラー時はNone）
        """
        try:
            if mode == "api":
                api_config = config.get("api", {})
                provider = api_config.get("provider", "openai")

                if provider == "openai":
                    return OpenAIClient(api_config)
                elif provider == "anthropic":
                    return AnthropicClient(api_config)
                elif provider == "custom":
                    # カスタムエンドポイントはOpenAI互換形式を想定
                    return OpenAIClient(api_config)
                else:
                    logger.error(f"サポートされていないAPIプロバイダー: {provider}")
                    return None

            elif mode == "local":
                local_config = config.get("local", {})
                return LocalLLMClient(local_config)
            else:
                logger.error(f"サポートされていないモード: {mode}")
                return None

        except ImportError as e:
            logger.warning(f"必要なパッケージがインストールされていません: {e}")
            return None
        except Exception as e:
            logger.error(f"LLMクライアントの作成に失敗しました: {e}")
            return None

    @staticmethod
    def create_client_with_fallback(
        config: Dict[str, Any], preferred_mode: str = "api"
    ) -> Optional[BaseLLMClient]:
        """
        LLMクライアントを作成（フォールバック付き）

        Args:
            config: LLM設定辞書
            preferred_mode: 優先するモード（'api' または 'local'）

        Returns:
            LLMクライアントインスタンス（エラー時はNone）
        """
        # 優先モードを試す
        client = LLMClientFactory.create_client(config, preferred_mode)
        if client:
            return client

        # フォールバック: もう一方のモードを試す
        fallback_mode = "local" if preferred_mode == "api" else "api"
        logger.info(
            f"{preferred_mode}モードが失敗したため、{fallback_mode}モードを試します..."
        )
        return LLMClientFactory.create_client(config, fallback_mode)
