"""
ドキュメント生成モジュール
"""

from pathlib import Path
from typing import Any

from .generator_factory import GeneratorFactory
from .utils.logger import get_logger

logger = get_logger("document_generator")


class DocumentGenerator:
    """ドキュメント生成クラス"""

    def __init__(
        self,
        project_root: Path,
        detected_languages: list[str],
        config: dict[str, Any],
        detected_package_managers: dict[str, str] | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトルートパス
            detected_languages: 検出された言語リスト
            config: 設定辞書
            detected_package_managers: 検出されたパッケージマネージャ辞書
        """
        self.project_root = project_root
        self.detected_languages = detected_languages
        self.config = config
        self.detected_package_managers = detected_package_managers or {}

    def generate_documents(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        if not self.detected_languages:
            logger.warning("サポートされている言語が検出されませんでした")
            return False

        success = True
        generators_to_run = []

        # 実行するジェネレーターを決定
        if self.config.get("generation", {}).get("generate_api_doc", True):
            generators_to_run.append(("api", "APIドキュメント"))
        if self.config.get("generation", {}).get("update_readme", True):
            generators_to_run.append(("readme", "README"))
        if self.config.get("generation", {}).get("generate_agents_doc", True):
            generators_to_run.append(("agents", "AGENTS.md"))

        # 各ジェネレーターを実行
        for gen_type, gen_name in generators_to_run:
            logger.info(f"[{gen_name}生成]")
            try:
                generator = GeneratorFactory.create_generator(
                    gen_type,
                    self.project_root,
                    self.detected_languages,
                    self.config,
                    self.detected_package_managers,
                )
                if generator.generate():
                    logger.info(f"✓ {gen_name}を生成しました")
                else:
                    logger.error(f"✗ {gen_name}の生成に失敗しました")
                    success = False
            except Exception as e:
                logger.error(f"✗ {gen_name}の生成中にエラーが発生しました: {e}", exc_info=True)
                success = False

        return success
