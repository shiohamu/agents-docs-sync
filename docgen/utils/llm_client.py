"""
LLMクライアントモジュール
OpenAI、Anthropic、ローカルLLM（Ollama、LM Studio）に対応
"""

from abc import ABC, abstractmethod
import os
import time
from typing import Any

from ..models import LLMClientConfig, LLMConfig
from ..utils.exceptions import ConfigError
from ..utils.logger import get_logger

logger = get_logger("llm_client")


class BaseLLMClient(ABC):
    """LLMクライアントの抽象基底クラス"""

    def __init__(self, config: dict[str, Any] | LLMConfig):
        """
        初期化

        Args:
            config: LLM設定辞書またはLLMConfigオブジェクト
        """
        if isinstance(config, dict):
            self.config = LLMConfig(**config)
        else:
            self.config = config

        self.timeout: int = self.config.timeout
        self.max_retries: int = self.config.max_retries
        self.retry_delay: float = self.config.retry_delay

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str | None:
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
        if last_exception:
            raise last_exception
        else:
            raise RuntimeError("LLM呼び出しで不明なエラーが発生しました")


class OpenAIClient(BaseLLMClient):
    """OpenAI APIクライアント"""

    def __init__(self, config: dict[str, Any]):
        # OpenAIクライアント用にproviderを設定
        if isinstance(config, dict):
            config["provider"] = "openai"
        super().__init__(config)
        try:
            import openai

            self.client: openai.OpenAI = openai.OpenAI(
                api_key=os.getenv(self.config.api_key_env or "OPENAI_API_KEY", ""),
                base_url=self.config.base_url,  # カスタムエンドポイント対応
            )
            self.model: str = self.config.model or "gpt-4o"
        except ImportError:
            raise ImportError(
                "openaiパッケージが必要です。`pip install openai`でインストールしてください。"
            ) from None
        except Exception as e:
            raise ConfigError(f"OpenAIクライアントの初期化に失敗しました: {e}") from e

    def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str | None:
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

            if response and response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            return None
        except Exception as e:
            logger.error(f"OpenAI API呼び出しエラー: {e}")
            return None

    def _create_outlines_model_internal(self, outlines):
        """OpenAI用のOutlinesモデルを作成"""
        return outlines.from_openai(self.client, self.model)


class AnthropicClient(BaseLLMClient):
    """Anthropic APIクライアント"""

    def __init__(self, config: dict[str, Any]):
        # Anthropicクライアント用にproviderを設定
        if isinstance(config, dict):
            config["provider"] = "anthropic"
        super().__init__(config)
        try:
            import anthropic

            self.client = anthropic.Anthropic(
                api_key=os.getenv(self.config.api_key_env or "ANTHROPIC_API_KEY", "")
            )
            self.model = self.config.model or "claude-3-5-sonnet-20241022"
        except ImportError:
            raise ImportError(
                "anthropicパッケージが必要です。`pip install anthropic`でインストールしてください。"
            ) from None
        except Exception as e:
            raise ConfigError(f"Anthropicクライアントの初期化に失敗しました: {e}") from e

    def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str | None:
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

            response = self._retry_with_backoff(self.client.messages.create, **api_kwargs)

            if response and response.content:
                # Anthropicのレスポンス形式に合わせて処理
                text_content = ""
                for block in response.content:
                    if hasattr(block, "text") and block.text:
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


class LocalLLMClient(BaseLLMClient):
    """ローカルLLMクライアント（Ollama、LM Studio対応）"""

    def __init__(self, config: dict[str, Any]):
        # LocalLLMクライアント用にproviderを設定（既に設定されている場合は上書きしない）
        if isinstance(config, dict) and "provider" not in config:
            config["provider"] = "local"
        super().__init__(config)
        try:
            import httpx

            self.httpx = httpx
        except ImportError:
            raise ImportError(
                "httpxパッケージが必要です。`pip install httpx`でインストールしてください。"
            ) from None

        self.base_url: str = self.config.base_url or "http://localhost:11434"
        self.model: str = config.get("model", "llama3")
        self.provider: str = config.get("provider", "ollama")

        # ベースURLの正規化（末尾のスラッシュを削除）
        self.base_url = self.base_url.rstrip("/")

    def generate(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str | None:
        """ローカルLLMを使用してテキストを生成"""
        try:
            # LocalLLMClientは常にローカルプロバイダーとして動作
            if self.config.provider == "ollama":
                return self._generate_ollama(prompt, system_prompt, **kwargs)
            elif self.config.provider in ["lmstudio", "custom", "local"]:
                return self._generate_openai_compatible(prompt, system_prompt, **kwargs)
            else:
                raise ConfigError(f"サポートされていないプロバイダー: {self.config.provider}")
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
        self, prompt: str, system_prompt: str | None = None, **kwargs
    ) -> str | None:
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
                logger.error(f"Ollama APIエラー: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Ollama API呼び出しエラー: {e}")
            return None

    def _generate_openai_compatible(
        self, prompt: str, system_prompt: str | None = None, **kwargs
    ) -> str | None:
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
                logger.error(f"OpenAI互換APIエラー: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"OpenAI互換API呼び出しエラー: {e}")
            return None


class LLMClientFactory:
    """LLMクライアントのファクトリークラス"""

    @staticmethod
    def create_client(
        config: dict[str, Any] | LLMClientConfig, mode: str = "api"
    ) -> BaseLLMClient | None:
        """
        LLMクライアントを作成

        Args:
            config: LLM設定辞書またはLLMClientConfigオブジェクト
            mode: 'api' または 'local'

        Returns:
            LLMクライアントインスタンス（エラー時はNone）
        """
        try:
            if mode == "api":
                if isinstance(config, LLMClientConfig):
                    client_config = config.openai or config.anthropic
                    if not client_config:
                        logger.error("API設定が見つかりません")
                        return None

                    provider = client_config.provider
                    if provider == "openai":
                        return OpenAIClient(client_config.model_dump())
                    elif provider == "anthropic":
                        return AnthropicClient(client_config.model_dump())
                    else:
                        logger.error(f"サポートされていないAPIプロバイダー: {provider}")
                        return None
                else:
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
        config: dict[str, Any], preferred_mode: str = "api"
    ) -> BaseLLMClient | None:
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
        logger.info(f"{preferred_mode}モードが失敗したため、{fallback_mode}モードを試します...")
        return LLMClientFactory.create_client(config, fallback_mode)
