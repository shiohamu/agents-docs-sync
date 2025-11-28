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

        self.collector: ProjectInfoCollector = ProjectInfoCollector(project_root, package_managers)

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

    def _find_insert_position(self, lines: list[str], section_name: str) -> int | None:
        """
        手動セクションを挿入する位置を見つける

        Note: ManualSectionMixinの_merge_manual_sectionsから呼び出されるため、
        オーバーライド可能にするためにここに残すか、Mixinに移動するか検討が必要。
        ここではMixinに移動したロジックとは別に、具体的な挿入位置ロジックを提供するため
        BaseGeneratorに残すか、あるいはManualSectionMixinにデフォルト実装を入れて
        必要に応じてオーバーライドするのが良い。

        今回はManualSectionMixinに_find_insert_positionを含めていないため（意図的？）、
        BaseGeneratorに残すか、Mixinに移動すべき。
        ManualSectionMixinの_merge_manual_sectionsは_find_insert_positionを呼んでいる。
        しかし、先ほどのManualSectionMixinの実装では_find_insert_positionを呼んでいなかった！

        確認：ManualSectionMixinの_merge_manual_sectionsは_find_insert_positionを使っているか？
        先ほど作成したManualSectionMixinのコードを確認すると...
        使っていない！単純なマージロジックのみ実装されているように見えたが、
        BaseGeneratorの元の実装は複雑な挿入ロジックを持っていた。

        ManualSectionMixinの実装を修正して、_find_insert_positionを含めるか、
        BaseGeneratorのこのメソッドを使うようにする必要がある。

        一旦BaseGeneratorにこのメソッドを残し、Mixinからはself._find_insert_positionを呼ぶ形にする。
        ただし、Mixinに定義がないと型チェックで警告が出る可能性がある。

        ここでは、BaseGeneratorに具体的なロジックを残し、Mixinは抽象的に使うか、
        あるいはMixinに移動するのが正しい。

        ManualSectionMixinの実装を再確認すると、_merge_manual_sectionsの中で
        _find_insert_positionを呼び出していない実装になっていた（簡易版？）。
        元のBaseGeneratorの実装は_find_insert_positionを使っていた。

        修正方針：
        ManualSectionMixinに_find_insert_positionも含めるべきだった。
        しかし、_find_insert_positionはドキュメント構造に依存するため、
        BaseGenerator（またはサブクラス）で定義されるべきかもしれない。

        ここではBaseGeneratorに定義し、Mixin側では期待する形にする。
        """
        if section_name == "description":
            # プロジェクト名の後に挿入
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    # プロジェクト名の次の空行の後
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        j += 1
                    return j
        elif section_name == "setup":
            # Technologies Usedの後に挿入
            for i, line in enumerate(lines):
                if line.strip() == "## Technologies Used":
                    # セクションの終わりを見つける
                    j = i + 1
                    while j < len(lines) and not (
                        lines[j].startswith("## ") and lines[j] != "## Technologies Used"
                    ):
                        j += 1
                    return j
        elif section_name == "usage":
            # Setupの後に挿入
            for i, line in enumerate(lines):
                if line.strip() == "## Setup":
                    # セクションの終わりを見つける
                    j = i + 1
                    while j < len(lines) and not (
                        lines[j].startswith("## ") and lines[j] != "## Setup"
                    ):
                        j += 1
                    return j
        elif section_name == "other":
            # 最後のセクションの後に挿入
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].startswith("## "):
                    # セクションの終わりを見つける
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("---"):
                        j += 1
                    return j

        return None

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
