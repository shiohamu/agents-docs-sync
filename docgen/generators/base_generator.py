"""
ベースジェネレーターモジュール
AGENTS.mdとREADME.mdのジェネレーターの共通部分を共通化

DI対応: サービスを使用して機能を提供。
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..models.project import ProjectInfo
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .services.formatting_service import FormattingService
    from .services.llm_service import LLMService
    from .services.manual_section_service import ManualSectionService
    from .services.rag_service import RAGService
    from .services.template_service import TemplateService


class BaseGenerator(ABC):
    """ベースジェネレータークラス（AGENTS.mdとREADME.mdの共通部分）

    DI対応: コンストラクタでサービスを注入可能。
    """

    def __init__(
        self,
        project_root: Path,
        languages: list[str],
        config: dict[str, Any],
        package_managers: dict[str, str] | None = None,
        *,
        # DI対応: オプショナルサービス注入
        llm_service: "LLMService | None" = None,
        template_service: "TemplateService | None" = None,
        rag_service: "RAGService | None" = None,
        formatting_service: "FormattingService | None" = None,
        manual_section_service: "ManualSectionService | None" = None,
    ):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
            package_managers: 検出されたパッケージマネージャの辞書
            llm_service: LLMサービス（DI）
            template_service: テンプレートサービス（DI）
            rag_service: RAGサービス（DI）
            formatting_service: フォーマットサービス（DI）
            manual_section_service: 手動セクションサービス（DI）
        """
        self.project_root: Path = project_root
        self.config: dict[str, Any] = config
        self.package_managers: dict[str, str] = package_managers or {}
        self.output_path: Path = self._get_output_path(config)
        self.logger = get_logger(self.__class__.__name__.lower())

        # 言語設定を適用（ignoredとpreferred）
        languages_config = config.get("languages", {})
        ignored_languages = set(languages_config.get("ignored", []))
        preferred_languages = languages_config.get("preferred", [])

        # ignored言語をフィルタリング
        filtered_languages = [lang for lang in languages if lang not in ignored_languages]

        # preferred言語に基づいて並び替え
        if preferred_languages:

            def sort_key(lang: str) -> tuple[int, str]:
                try:
                    index = preferred_languages.index(lang)
                    return (0, str(index))  # preferredに含まれる場合は(0, index)
                except ValueError:
                    return (1, lang)  # preferredに含まれない場合は(1, name)

            filtered_languages.sort(key=sort_key)
            if ignored_languages or preferred_languages:
                self.logger.debug(
                    f"言語設定を適用: ignored={ignored_languages}, "
                    f"preferred={preferred_languages}, "
                    f"結果={filtered_languages}"
                )

        self.languages: list[str] = filtered_languages

        # プロジェクト情報収集器
        from ..collectors.project_info_collector import ProjectInfoCollector

        # exclude設定を取得してProjectInfoCollectorに渡す
        exclude_config = config.get("exclude", {})
        exclude_directories = exclude_config.get("directories", [])

        self.collector: ProjectInfoCollector = ProjectInfoCollector(
            project_root,
            package_managers,
            logger=self.logger,
            exclude_directories=exclude_directories,
        )

        # AGENTS設定
        self.agents_config: dict[str, Any] = config.get("agents", {})

        # サービス初期化（注入されない場合はデフォルト生成）
        from .service_factory import GeneratorServiceFactory

        self.llm_service = llm_service or GeneratorServiceFactory.create_llm_service(
            config, self.logger
        )
        self.template_service = (
            template_service or GeneratorServiceFactory.create_template_service()
        )
        self.rag_service = rag_service or GeneratorServiceFactory.create_rag_service(
            project_root, config, self.logger
        )
        self.formatting_service = (
            formatting_service or GeneratorServiceFactory.create_formatting_service()
        )
        self.manual_section_service = (
            manual_section_service or GeneratorServiceFactory.create_manual_section_service()
        )

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
            return self.manual_section_service.extract(content)
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
                markdown = self.manual_section_service.merge(markdown, manual_sections)

            # 検証
            if not self.formatting_service.validate_output(markdown):
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

    def _get_architecture_diagram_content(self) -> str:
        """アーキテクチャ図のコンテンツを取得"""
        arch_config = self.config.get("architecture", {})

        if not arch_config.get("enabled", False):
            return ""

        try:
            # 遅延インポートで循環参照を回避
            from ..archgen.renderer import ArchitectureRenderer
            from ..archgen.scanner import ProjectScanner

            # 出力ディレクトリの決定
            output_dir_str = arch_config.get("output_dir", "docs/architecture")
            output_dir = self.project_root / output_dir_str

            # スキャナーとレンダラーの初期化
            exclude_dirs = self.config.get("exclude", {}).get("directories", [])
            scanner = ProjectScanner(
                self.project_root, exclude_directories=exclude_dirs, config=self.config
            )
            manifest = scanner.scan()
            self.logger.info(
                f"Architecture scan result: {len(manifest.services)} services detected"
            )

            renderer = ArchitectureRenderer(
                generator_type=arch_config.get("generator", "mermaid"),
                image_formats=arch_config.get("image_formats", ["png"]),
            )

            # レンダリング実行
            generated_files = renderer.render(manifest, output_dir)
            self.logger.info(f"Architecture render result: {generated_files}")

            # Markdownファイルのパスを取得
            markdown_path = generated_files.get("markdown")
            if markdown_path and markdown_path.exists():
                # Markdownファイルの内容を読み込む
                content = markdown_path.read_text(encoding="utf-8")

                # Servicesセクションのみを抽出
                services_section = self._extract_services_section(content)
                if services_section:
                    return services_section

                # フォールバック: 最初のH1見出しを除去して返す（後方互換性）
                lines = content.splitlines()
                filtered_lines = []
                found_title = False
                for line in lines:
                    if not found_title and line.strip().startswith("# "):
                        found_title = True
                        continue
                    filtered_lines.append(line)

                return "\n".join(filtered_lines).strip()

            self.logger.warning(f"Architecture markdown file not found at {markdown_path}")
            return ""

        except Exception as e:
            self.logger.warning(f"アーキテクチャ図の生成/取得に失敗しました: {e}", exc_info=True)
            return ""

    def _generate_key_features(
        self, project_info: ProjectInfo, prompt_file: str = "agents_prompts.toml"
    ) -> list[str]:
        """主要機能を生成

        Args:
            project_info: プロジェクト情報
            prompt_file: プロンプトファイル名（デフォルト: agents_prompts.toml）

        Returns:
            主要機能のリスト
        """
        if not self._should_use_llm():
            return []

        content = self._generate_content_with_llm(prompt_file, "key_features", project_info)

        # コンテンツをリストに変換
        if isinstance(content, list):
            return content

        # 文字列の場合は行ごとに分割してリスト化
        return [line.strip("- ") for line in content.splitlines() if line.strip()]

    def _generate_architecture(
        self, project_info: ProjectInfo, prompt_file: str = "agents_prompts.toml"
    ) -> str:
        """アーキテクチャを生成

        Args:
            project_info: プロジェクト情報
            prompt_file: プロンプトファイル名（デフォルト: agents_prompts.toml）

        Returns:
            アーキテクチャの説明文字列
        """
        # 設定ベースのアーキテクチャ図生成を試みる
        arch_content = self._get_architecture_diagram_content()
        if arch_content:
            return arch_content

        if not self._should_use_llm():
            return ""

        return self._generate_content_with_llm(prompt_file, "architecture", project_info)

    def _should_use_llm(self) -> bool:
        """LLMを使用すべきかどうかを判定

        Returns:
            LLMを使用する場合True
        """
        generation_config = self.agents_config.get("generation", {})
        mode = generation_config.get(self._get_mode_key(), "template")
        return mode in ("llm", "hybrid")

    def _generate_content_with_llm(
        self, prompt_file: str, section: str, project_info: ProjectInfo
    ) -> Any:
        """LLMでコンテンツを生成

        Args:
            prompt_file: プロンプトファイル名
            section: セクション名
            project_info: プロジェクト情報

        Returns:
            生成されたコンテンツ
        """
        # サブクラスで実装される想定だが、デフォルト実装を提供
        self.logger.warning(
            f"_generate_content_with_llm is not implemented in {self.__class__.__name__}"
        )
        return ""

    def _generate_with_llm(self, project_info: ProjectInfo) -> str:
        """LLMでドキュメント全体を生成

        Args:
            project_info: プロジェクト情報

        Returns:
            生成されたマークダウン
        """
        # サブクラスで実装される想定だが、デフォルト実装を提供
        self.logger.warning(f"_generate_with_llm is not implemented in {self.__class__.__name__}")
        return self._generate_template(project_info)

    def _generate_hybrid(self, project_info: ProjectInfo) -> str:
        """ハイブリッド方式でドキュメントを生成

        Args:
            project_info: プロジェクト情報

        Returns:
            生成されたマークダウン
        """
        # サブクラスで実装される想定だが、デフォルト実装を提供
        self.logger.warning(f"_generate_hybrid is not implemented in {self.__class__.__name__}")
        return self._generate_template(project_info)

    def _extract_services_section(self, content: str) -> str | None:
        """
        アーキテクチャ図のMarkdownからServicesセクションのみを抽出

        Args:
            content: Markdownファイルの内容

        Returns:
            Servicesセクションの内容（見つからない場合はNone）
        """
        lines = content.splitlines()
        services_start = None
        services_end = None
        in_code_block = False

        # Servicesセクションの開始位置を探す
        for i, line in enumerate(lines):
            # コードブロックの開始/終了を検出
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # コードブロック内はスキップ
            if in_code_block:
                continue

            # Servicesセクションの開始（## Services または ## サービス）
            if line.strip().startswith("## ") and ("Services" in line or "サービス" in line):
                services_start = i
                break

        if services_start is None:
            return None

        # Servicesセクションの終了位置を探す（次の## セクションまたはファイル終端）
        for i in range(services_start + 1, len(lines)):
            line = lines[i]
            # コードブロックの開始/終了を検出
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # コードブロック内は含める
            if in_code_block:
                continue

            # 次のセクション（## で始まる）が見つかったら終了
            if line.strip().startswith("## "):
                services_end = i
                break

        # Servicesセクションを抽出
        if services_end is not None:
            services_lines = lines[services_start:services_end]
        else:
            services_lines = lines[services_start:]

        return "\n".join(services_lines).strip()
