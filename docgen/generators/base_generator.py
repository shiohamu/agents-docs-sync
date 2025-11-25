"""
ベースジェネレーターモジュール
AGENTS.mdとREADME.mdのジェネレーターの共通部分を共通化
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..models.project import ProjectInfo
from ..utils.llm_client import LLMClientFactory
from ..utils.logger import get_logger
from ..utils.markdown_utils import UNKNOWN, get_current_timestamp


class BaseGenerator(ABC):
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

    def _generate_footer(self) -> str:
        """フッターを生成"""
        return f"*この{self._get_document_type()}は自動生成されています。最終更新: {get_current_timestamp()}*"

    def _extract_description_section(self, content: str) -> str:
        """
        Extract description section from content

        Args:
            content: Document content

        Returns:
            Description section text
        """
        from ..utils.markdown_utils import DESCRIPTION_END, DESCRIPTION_START

        lines = content.split("\n")
        description_lines = []
        in_description = False

        for line in lines:
            if DESCRIPTION_START in line:
                in_description = True
                continue
            elif DESCRIPTION_END in line:
                break
            elif in_description:
                description_lines.append(line)

        return "\n".join(description_lines)

    @abstractmethod
    def _get_structured_model(self) -> Any:
        """構造化モデルを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _create_llm_prompt(self, project_info: ProjectInfo) -> str:
        """LLM用のプロンプトを作成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_template(self, project_info: ProjectInfo) -> str:
        """テンプレートベースでマークダウンを生成（サブクラスで実装）"""
        pass

    def _generate_custom_instructions_section(
        self, custom_instructions: str | dict[str, Any]
    ) -> list[str]:
        """カスタム指示セクションを生成"""
        lines = []
        lines.append("## プロジェクト固有の指示")
        lines.append("")

        if isinstance(custom_instructions, str):
            lines.append(custom_instructions)
        elif isinstance(custom_instructions, dict):
            # dictの場合はキーをセクションとして扱う
            for key, value in custom_instructions.items():
                lines.append(f"### {key}")
                lines.append("")
                lines.append(str(value))
                lines.append("")

        lines.append("")
        return lines

    def _extract_manual_sections_from_existing(self) -> dict[str, str]:
        """既存ファイルから手動セクションを抽出"""
        if not self.output_path.exists():
            return {}
        try:
            content = self.output_path.read_text(encoding="utf-8")
            return self._extract_manual_sections(content)
        except Exception:
            return {}

    def _extract_manual_sections(self, content: str) -> dict[str, str]:
        """
        既存のドキュメントから手動セクションを抽出

        Args:
            content: ドキュメントの内容

        Returns:
            セクション名をキー、手動内容を値とする辞書
        """
        import re

        sections = {}

        # Find manual section markers
        from ..utils.markdown_utils import MANUAL_MARKER_REGEX

        for match in MANUAL_MARKER_REGEX.finditer(content):
            section_name = match.group(1)
            section_content = match.group(2).strip()
            # Remove nested manual markers
            section_content = re.sub(
                r"<!--\s*MANUAL_START:\w+\s*-->|<!--\s*MANUAL_END:\w+\s*-->", "", section_content
            ).strip()
            sections[section_name] = section_content

        return sections

    def _merge_manual_sections(self, markdown: str, manual_sections: dict[str, str]) -> str:
        """
        生成されたマークダウンに手動セクションをマージ

        Args:
            markdown: 生成されたマークダウン
            manual_sections: 手動セクションの辞書

        Returns:
            マージされたマークダウン
        """
        if not manual_sections:
            return markdown

        lines = markdown.split("\n")
        result = []
        i = 0
        inserted_sections = set()

        while i < len(lines):
            line = lines[i]
            result.append(line)

            # MANUAL_STARTマーカーを見つけたら、手動内容を挿入
            if line.strip().startswith("<!-- MANUAL_START:"):
                section_name = line.strip().split(":", 1)[1].split("-->", 1)[0].strip()
                if section_name in manual_sections:
                    # MANUAL_STARTの次の空行をスキップ
                    i += 1
                    if i < len(lines) and lines[i].strip() == "":
                        i += 1
                    # 手動内容を挿入
                    manual_content = manual_sections[section_name]
                    result.extend(manual_content.split("\n"))
                    # MANUAL_ENDまでスキップ
                    while i < len(lines) and not lines[i].strip().startswith("<!-- MANUAL_END:"):
                        i += 1
                    if i < len(lines):
                        result.append(lines[i])  # MANUAL_ENDを追加
                    inserted_sections.add(section_name)
                else:
                    # 手動セクションがない場合、次の行を処理
                    pass
            i += 1

        # 挿入されていない手動セクションを適切な位置に追加
        for section_name, manual_content in manual_sections.items():
            if section_name not in inserted_sections:
                # セクションに応じた挿入位置を決定
                insert_position = self._find_insert_position(result, section_name)
                if insert_position is not None:
                    # MANUAL_START/ENDを追加して挿入
                    manual_lines = [
                        "",
                        f"<!-- MANUAL_START:{section_name} -->",
                        manual_content,
                        f"<!-- MANUAL_END:{section_name} -->",
                        "",
                    ]
                    result[insert_position:insert_position] = manual_lines

        return "\n".join(result)

    def _find_insert_position(self, lines: list[str], section_name: str) -> int | None:
        """
        手動セクションを挿入する位置を見つける

        Args:
            lines: マークダウンの行リスト
            section_name: セクション名

        Returns:
            挿入位置（行インデックス）、見つからない場合はNone
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

    def _generate_with_llm(self, project_info: ProjectInfo) -> str:
        """
        LLMを使用してドキュメントを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列（エラー時はテンプレート生成にフォールバック）
        """
        try:
            return self._generate_with_outlines(project_info)

        except Exception as e:
            self.logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _should_use_outlines(self) -> bool:
        """
        Outlinesを使用するかどうかを判定

        Returns:
            Outlinesを使用するかどうか
        """
        from ..utils.outlines_utils import should_use_outlines

        return should_use_outlines(self.agents_config)

    def _get_llm_client_with_fallback(self) -> Any:
        """
        LLMクライアントを取得（フォールバック付き）

        Returns:
            LLMクライアント（取得できない場合はNone）
        """
        llm_mode = self.agents_config.get("llm_mode", "api")
        preferred_mode = "api" if llm_mode in "api" else "local"

        return LLMClientFactory.create_client_with_fallback(
            self.agents_config, preferred_mode=preferred_mode
        )

    def _generate_with_outlines(self, project_info: ProjectInfo) -> str:
        """
        Outlinesを使用して構造化されたドキュメントを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        try:
            # LLMクライアントを取得
            client = self._get_llm_client_with_fallback()

            if not client:
                self.logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # Outlinesモデルを作成
            outlines_model = self._create_outlines_model(client)

            if outlines_model is None:
                # Outlinesがサポートされていない場合、テンプレート生成にフォールバック
                self.logger.info(
                    "Outlinesがサポートされていないため、テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info)

            # 構造化出力モデルで生成
            self.logger.info("Outlinesを使用して構造化されたドキュメントを生成中...")
            structured_data = outlines_model(prompt, self._get_structured_model())

            # 構造化データをマークダウンに変換
            markdown = self._convert_structured_data_to_markdown(structured_data, project_info)

            return markdown

        except Exception as e:
            self.logger.error(
                f"Outlines生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _create_outlines_model(self, client):
        """
        Outlinesモデルを作成

        Args:
            client: LLMクライアント

        Returns:
            Outlinesモデル
        """
        from ..utils.outlines_utils import create_outlines_model

        return create_outlines_model(client)

    def _generate_hybrid(self, project_info: ProjectInfo) -> str:
        """
        テンプレートとLLMを組み合わせて生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # まずテンプレートを生成
        template_content = self._generate_template(project_info)

        try:
            # プロジェクト概要セクションのみLLMで改善
            existing_overview = self._get_project_overview_section(template_content)
            improved_overview = self._generate_overview_with_llm(
                project_info, existing_overview
            )

            if improved_overview and improved_overview != existing_overview:
                return self._replace_overview_section(template_content, improved_overview)
            else:
                return template_content

        except Exception as e:
            self.logger.warning(
                f"ハイブリッド生成中にエラーが発生しました: {e}。テンプレートのみを使用します。",
                exc_info=True,
            )
            return template_content

    def _replace_overview_section(self, content: str, new_overview: str) -> str:
        """
        プロジェクト概要セクションを置き換え（サブクラスでオーバーライド可能）

        Args:
            content: 元のコンテンツ
            new_overview: 新しい概要

        Returns:
            置き換え後のコンテンツ
        """
        import re

        # デフォルト実装: "## プロジェクト概要" または "## 概要" セクションを置き換え
        # パターン: ヘッダーから次のセクション（## で始まる行）の前まで
        pattern = r"(## (プロジェクト概要|概要)\s*\n)(.*?)(\n## )"
        replacement = r"\1\n" + new_overview + r"\3"

        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # デバッグ: 置換が成功したか確認
        if updated_content == content:
            self.logger.warning(
                "Overview section replacement did not match. Pattern may need adjustment."
            )
        else:
            self.logger.debug("Overview section successfully replaced.")

        return updated_content

    def _generate_overview_with_llm(
        self, project_info: ProjectInfo, existing_overview: str
    ) -> str | None:
        """
        LLMを使用してプロジェクト概要を生成

        Args:
            project_info: プロジェクト情報
            existing_overview: 既存の概要

        Returns:
            改善された概要（生成失敗時はNone）
        """
        try:
            # LLMクライアントを取得
            client = self._get_llm_client_with_fallback()

            if not client:
                self.logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレートのみを使用します。"
                )
                return None

            prompt = self._create_overview_prompt(project_info, existing_overview)

            system_prompt = """あなたは技術ドキュメント作成の専門家です。プロジェクト概要を明確で有用な形で記述してください。
最終的な出力のみを生成し、思考過程や試行錯誤の痕跡を含めないでください。"""

            self.logger.info("LLMを使用してプロジェクト概要セクションを改善中...")
            improved_overview = client.generate(prompt, system_prompt=system_prompt)

            if improved_overview:
                # LLM出力をクリーンアップ
                cleaned_overview = self._clean_llm_output(improved_overview)

                # 出力を検証
                if not self._validate_output(cleaned_overview):
                    self.logger.warning(
                        "LLM出力の検証に失敗しました。テンプレートのみを使用します。"
                    )
                    return None

                return cleaned_overview
            else:
                return None
        except Exception as e:
            self.logger.warning(
                f"概要生成中にエラーが発生しました: {e}",
                exc_info=True,
            )
            return None

    def _create_overview_prompt(self, project_info: ProjectInfo, existing_overview: str) -> str:
        """
        プロジェクト概要生成用のプロンプトを作成（サブクラスでオーバーライド可能）

        Args:
            project_info: プロジェクト情報
            existing_overview: 既存の概要（テンプレート生成結果）

        Returns:
            プロンプト文字列
        """
        return f"""以下のプロジェクト情報を基に、{self._get_document_type()}の「プロジェクト概要」セクションの内容を改善してください。
既存のテンプレート生成内容を参考に、より詳細で有用な説明を生成してください。

プロジェクト情報:
{self._format_project_info_for_prompt(project_info)}

既存のテンプレート生成内容:
{existing_overview}

改善されたプロジェクト概要の内容をマークダウン形式で出力してください。
ヘッダー（## プロジェクト概要）は含めないでください。内容のみを出力してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
手動セクション（<!-- MANUAL_START:description --> と <!-- MANUAL_END:description -->）は保持してください。"""

    def _format_project_info_for_prompt(self, project_info: ProjectInfo) -> str:
        """
        プロジェクト情報をプロンプト用にフォーマット

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            フォーマットされた文字列
        """
        lines = []
        lines.append(f"プロジェクト名: {self.project_root.name}")
        lines.append(f"使用言語: {', '.join(self.languages) if self.languages else UNKNOWN}")

        description = project_info.description
        if description:
            lines.append(f"説明: {description}")

        dependencies = project_info.dependencies or {}
        if dependencies:
            lines.append("依存関係:")
            for dep_type, deps in dependencies.items():
                lines.append(f"  - {dep_type}: {', '.join(deps[:10])}")

        build_commands = project_info.build_commands
        if build_commands:
            lines.append("ビルドコマンド:")
            for cmd in build_commands:
                lines.append(f"  - {cmd}")

        test_commands = project_info.test_commands
        if test_commands:
            lines.append("テストコマンド:")
            for cmd in test_commands:
                lines.append(f"  - {cmd}")

        coding_standards = project_info.coding_standards
        if coding_standards:
            lines.append("コーディング規約:")
            if coding_standards.get("formatter"):
                lines.append(f"  - フォーマッター: {coding_standards['formatter']}")
            if coding_standards.get("linter"):
                lines.append(f"  - リンター: {coding_standards['linter']}")
            if coding_standards.get("style_guide"):
                lines.append(f"  - スタイルガイド: {coding_standards['style_guide']}")

        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            lines.append(f"カスタム指示: {custom_instructions}")

        return "\n".join(lines)

    def _clean_llm_output(self, text: str) -> str:
        """
        LLMの出力から思考過程や試行錯誤の痕跡を削除

        Args:
            text: LLMで生成されたテキスト

        Returns:
            クリーンアップされたテキスト
        """
        from ..utils.outlines_utils import clean_llm_output

        return clean_llm_output(text)

    def _validate_output(self, text: str) -> bool:
        """
        LLMの出力を検証して、Pydanticモデルでパースできるかチェック

        Args:
            text: 検証するテキスト

        Returns:
            検証に合格したかどうか
        """
        from ..utils.outlines_utils import validate_output

        return validate_output(text)

    def _collect_project_description(self) -> str | None:
        """
        Collect project description
        """
        return self.collector.collect_project_description()

    def generate(self) -> bool:
        """
        ドキュメントを生成

        Returns:
            成功したかどうか
        """
        try:
            # 出力ディレクトリを作成
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            # プロジェクト情報を収集
            project_info = self.collector.collect_all()

            # マークダウンを生成
            markdown = self._generate_markdown(project_info)

            # 手動セクションをマージ
            manual_sections = self._extract_manual_sections_from_existing()
            merged_markdown = self._merge_manual_sections(markdown, manual_sections)

            # ファイルに書き込み
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(merged_markdown)

            return True
        except Exception as e:
            self.logger.error(
                f"{self._get_document_type()}生成中に予期しないエラーが発生しました: {e}",
                exc_info=True,
            )
            return False

    def _render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """
        Jinja2テンプレートをレンダリング

        Args:
            template_name: テンプレートファイル名（templates/配下）
            context: テンプレートに渡す変数辞書

        Returns:
            レンダリングされた文字列

        Raises:
            Exception: テンプレート読み込みまたはレンダリングエラー
        """
        from importlib import resources

        import jinja2

        try:
            # テンプレートファイルを読み込み
            template_content = (
                resources.files("docgen.templates")
                .joinpath(template_name)
                .read_text(encoding="utf-8")
            )

            # Jinja2テンプレートを作成
            template = jinja2.Template(template_content)

            # コンテキストでレンダリング
            return template.render(**context)

        except FileNotFoundError:
            self.logger.error(f"テンプレートファイルが見つかりません: {template_name}")
            raise
        except jinja2.TemplateError as e:
            self.logger.error(f"テンプレートレンダリングエラー: {e}")
            raise
        except Exception as e:
            self.logger.error(f"予期しないエラー: {e}")
            raise
