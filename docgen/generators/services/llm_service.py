"""
LLM Service

LLMを使用したコンテンツ生成サービス。
MixinパターンからDIへの移行に対応。
"""

from logging import Logger
from typing import Any

from docgen.utils.llm import LLMClientFactory
from docgen.utils.logger import get_logger


class LLMService:
    """LLM生成サービス"""

    def __init__(
        self,
        config: dict[str, Any],
        logger: Logger | None = None,
    ):
        """
        初期化

        Args:
            config: 設定辞書（agents設定を含む）
            logger: ロガー
        """
        self._config = config
        self._logger = logger or get_logger("llm_service")
        self._client: Any = None

    @property
    def agents_config(self) -> dict[str, Any]:
        """agents設定を取得"""
        return self._config.get("agents", {})

    def get_client(self) -> Any:
        """
        LLMクライアントを取得（フォールバック付き）

        Returns:
            LLMクライアント（取得できない場合はNone）
        """
        if self._client is not None:
            return self._client

        llm_mode = self.agents_config.get("llm_mode", "api")
        preferred_mode = "api" if llm_mode == "api" else "local"

        self._client = LLMClientFactory.create_client_with_fallback(
            self.agents_config, preferred_mode=preferred_mode
        )
        return self._client

    def generate(self, prompt: str) -> str:
        """
        LLMを使用してテキストを生成

        Args:
            prompt: 入力プロンプト

        Returns:
            生成されたテキスト

        Raises:
            RuntimeError: LLMクライアントが利用できない場合
        """
        client = self.get_client()
        if not client:
            raise RuntimeError("LLMクライアントが利用できません")

        return client.generate(prompt)

    def should_use_outlines(self) -> bool:
        """
        Outlinesを使用するかどうかを判定

        Returns:
            Outlinesを使用するかどうか
        """
        from docgen.generators.utils.outlines_utils import should_use_outlines

        return should_use_outlines(self.agents_config)

    def create_outlines_model(self, client: Any) -> Any:
        """
        Outlinesモデルを作成

        Args:
            client: LLMクライアント

        Returns:
            Outlinesモデル（サポートされない場合はNone）
        """
        from docgen.generators.utils.outlines_utils import create_outlines_model

        return create_outlines_model(client)
