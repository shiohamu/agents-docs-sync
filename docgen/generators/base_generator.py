"""
ベースジェネレーターモジュール
AGENTS.mdとREADME.mdのジェネレーターの共通部分を共通化
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..models.project import ProjectInfo
from ..utils.logger import get_logger
from .mixins.llm_mixin import LLMMixin
from .mixins.manual_section_mixin import ManualSectionMixin
from .mixins.markdown_mixin import MarkdownMixin
from .mixins.rag_mixin import RAGMixin
from .mixins.template_mixin import TemplateMixin


class BaseGenerator(
    LLMMixin,
    TemplateMixin,
    ManualSectionMixin,
    RAGMixin,
    MarkdownMixin,
    ABC,
):
    """ベースジェネレータークラス（AGENTS.mdとREADME.mdの共通部分）"""

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
            package_managers: 検出されたパッケージマネージャの辞書
        """
        self.project_root: Path = project_root
        self.languages: list[str] = languages
        self.config: dict[str, Any] = config
        self.package_managers: dict[str, str] = package_managers or {}
        self.output_path: Path = self._get_output_path(config)
        self.logger = get_logger(self.__class__.__name__.lower())

        # プロジェクト情報収集器
        from ..collectors.project_info_collector import ProjectInfoCollector

        self.collector: ProjectInfoCollector = ProjectInfoCollector(
            project_root, package_managers, logger=self.logger
        )

        # AGENTS設定
        self.agents_config: dict[str, Any] = config.get("agents", {})

    @abstractmethod
    def _get_mode_key(self) -> str:
        """モードキーを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _get_output_key(self) -> str:
        """出力キーを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _get_document_type(self) -> str:
        """ドキュメントタイプを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _convert_structured_data_to_markdown(
        self, structured_data: Any, project_info: ProjectInfo
    ) -> str:
        """構造化データをマークダウンに変換（サブクラスで実装）"""
        pass

    @abstractmethod
    def _get_project_overview_section(self, content: str) -> str:
        """プロジェクト概要セクションを取得（サブクラスで実装）"""
        pass

    def _get_output_path(self, config: dict[str, Any]) -> Path:
        """出力パスを取得"""
        output_config = config.get("output", {})
        filename = output_config.get(self._get_output_key(), self._get_default_filename())
        output_path = Path(filename)
        if not output_path.is_absolute():
            output_path = self.project_root / output_path
        return output_path

    def _get_default_filename(self) -> str:
        """デフォルトファイル名を取得（サブクラスでオーバーライド可能）"""
        return f"{self._get_document_type()}"

    @abstractmethod
    def _get_structured_model(self) -> Any:
        """構造化モデルを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _create_llm_prompt(self, project_info: ProjectInfo, rag_context: str = "") -> str:
        """LLM用のプロンプトを作成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_template(self, project_info: ProjectInfo) -> str:
        """テンプレートベースでマークダウンを生成（サブクラスで実装）"""
        pass

    def _extract_manual_sections_from_existing(self) -> dict[str, str]:
        """既存ファイルから手動セクションを抽出"""
        if not self.output_path.exists():
            return {}
        try:
            content = self.output_path.read_text(encoding="utf-8")
            return self._extract_manual_sections(content)
        except Exception:
            return {}

    def _generate_markdown(self, project_info: ProjectInfo) -> str:
        """
        プロジェクト情報からマークダウンを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # 生成モードを取得（デフォルトは'template'）
        generation_config = self.agents_config.get("generation", {})
        mode = generation_config.get(self._get_mode_key(), "template")

        if mode == "llm":
            # LLM完全生成
            return self._generate_with_llm(project_info)
        elif mode == "hybrid":
            # ハイブリッド生成
            return self._generate_hybrid(project_info)
        else:
            # テンプレート生成（デフォルト）
            return self._generate_template(project_info)

    def generate(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            生成に成功した場合True
        """
        try:
            self.logger.info(f"[{self._get_document_type()}生成]")

            # プロジェクト情報を収集
            project_info = self.collector.collect_all()

            # 既存の手動セクションを抽出
            manual_sections = self._extract_manual_sections_from_existing()
            if manual_sections:
                self.logger.info(
                    f"既存の手動セクションを抽出しました: {list(manual_sections.keys())}"
                )

            # マークダウンを生成
            markdown = self._generate_markdown(project_info)

            # 手動セクションをマージ
            if manual_sections:
                markdown = self._merge_manual_sections(markdown, manual_sections)

            # 検証
            if not self._validate_output(markdown):
                self.logger.error("生成されたドキュメントが無効です")
                return False

            # ファイルに書き込み
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_text(markdown, encoding="utf-8")

            self.logger.info(f"✓ {self._get_document_type()}を生成しました")
            return True

        except Exception as e:
            self.logger.error(
                f"{self._get_document_type()}生成中にエラーが発生しました: {e}", exc_info=True
            )
            return False
