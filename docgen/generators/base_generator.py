"""
ベースジェネレーターモジュール
AGENTS.mdとREADME.mdのジェネレーターの共通部分を共通化
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..models import ProjectInfo
from ..utils.file_utils import safe_write_file
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
    def _get_output_path(self, config: dict[str, Any]) -> Path:
        """出力パスを取得（サブクラスで実装）"""
        pass

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
    def _get_project_overview_section(self, content: str) -> str:
        """プロジェクト概要セクションを取得（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_template(self, project_info: ProjectInfo) -> str:
        """テンプレートベースでマークダウンを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_project_overview(self, project_info: ProjectInfo) -> list[str]:
        """プロジェクト概要セクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_setup_section(self, project_info: ProjectInfo) -> list[str]:
        """開発環境セットアップセクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_build_test_section(self, project_info: ProjectInfo) -> list[str]:
        """ビルド/テストセクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_coding_standards_section(self, project_info: ProjectInfo) -> list[str]:
        """コーディング規約セクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_pr_section(self, project_info: ProjectInfo) -> list[str]:
        """プルリクエストセクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _generate_custom_instructions_section(
        self, custom_instructions: str | dict[str, Any]
    ) -> list[str]:
        """カスタム指示セクションを生成（サブクラスで実装）"""
        pass

    @abstractmethod
    def _convert_structured_data_to_markdown(self, data, project_info: ProjectInfo) -> str:
        """構造化データをマークダウン形式に変換（サブクラスで実装）"""
        pass

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

            # 既存の手動セクションを保持
            manual_sections = self._extract_manual_sections_from_existing()
            if manual_sections:
                markdown = self._merge_manual_sections(markdown, manual_sections)

            # ファイルに書き込み
            if not safe_write_file(self.output_path, markdown):
                return False

            return True
        except Exception as e:
            self.logger.error(f"ドキュメント生成に失敗しました: {e}", exc_info=True)
            return False

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

        lines = markdown.split("\n")
        result = []
        i = 0

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
                else:
                    # 手動セクションがない場合、次の行を処理
                    pass
            i += 1

        return "\n".join(result)

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
            # Outlinesを使用した構造化生成を試す
            if self._should_use_outlines():
                return self._generate_with_outlines(project_info)

            # 従来のLLM生成にフォールバック
            return self._generate_with_llm_legacy(project_info)

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
        # 設定でOutlinesが有効になっているかチェック
        from ..utils.outlines_utils import should_use_outlines

        return should_use_outlines(self.config)

    def _get_llm_client_with_fallback(self) -> Any:
        """
        LLMクライアントを取得（フォールバック付き）

        Returns:
            LLMクライアント（取得できない場合はNone）
        """
        llm_mode = self.agents_config.get("llm_mode", "api")
        preferred_mode = "api" if llm_mode in ["api", "both"] else "local"

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
                f"Outlines生成中にエラーが発生しました: {e}。従来のLLM生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_with_llm_legacy(project_info)

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

    def _generate_with_llm_legacy(self, project_info: ProjectInfo) -> str:
        """
        従来のLLM生成（Outlinesなし）

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

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info)

            # システムプロンプト
            system_prompt = f"""あなたは技術ドキュメント作成の専門家です。
{self._get_document_type()}ドキュメントを生成してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

            # LLMで生成
            self.logger.info(f"LLMを使用して{self._get_document_type()}を生成中...")
            generated_text = client.generate(prompt, system_prompt=system_prompt)

            if generated_text:
                # LLM出力をクリーンアップ
                cleaned_text = self._clean_llm_output(generated_text)

                # 出力を検証
                if not self._validate_output(cleaned_text):
                    self.logger.warning(
                        "LLM出力の検証に失敗しました。テンプレート生成にフォールバックします。"
                    )
                    return self._generate_template(project_info)

                # 生成されたテキストにタイムスタンプを追加
                lines = cleaned_text.split("\n")
                # フッターを追加（既に含まれていない場合）
                footer_text = self._generate_footer()
                if not any(footer_text.split("*")[1] in line for line in lines):
                    lines.append("")
                    lines.append(footer_text)
                return "\n".join(lines)
            else:
                self.logger.warning("LLM生成が空でした。テンプレート生成にフォールバックします。")
                return self._generate_template(project_info)

        except Exception as e:
            self.logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

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
            # LLMクライアントを取得
            llm_mode = self.agents_config.get("llm_mode", "api")
            preferred_mode = "api" if llm_mode in ["api", "both"] else "local"

            client = LLMClientFactory.create_client_with_fallback(
                self.agents_config, preferred_mode=preferred_mode
            )

            if not client:
                self.logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレートのみを使用します。"
                )
                return template_content

            # プロジェクト概要セクションのみLLMで改善
            prompt = f"""以下のプロジェクト情報を基に、{self._get_document_type()}の「プロジェクト概要」セクションの内容を改善してください。
既存のテンプレート生成内容を参考に、より詳細で有用な説明を生成してください。

プロジェクト情報:
{self._format_project_info_for_prompt(project_info)}

既存のテンプレート生成内容:
{self._get_project_overview_section(template_content)}

改善されたプロジェクト概要の内容をマークダウン形式で出力してください。
ヘッダー（## プロジェクト概要）は含めないでください。内容のみを出力してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
手動セクション（<!-- MANUAL_START:description --> と <!-- MANUAL_END:description -->）は保持してください。"""

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
                    return template_content

                # テンプレートのプロジェクト概要セクションを置き換え
                lines = template_content.split("\n")
                new_lines = []
                skip_until_end = False

                for _i, line in enumerate(lines):
                    if "## プロジェクト概要" in line:
                        new_lines.append(line)
                        new_lines.append("")
                        # 改善された概要を挿入
                        new_lines.extend(cleaned_overview.split("\n"))
                        skip_until_end = True
                    elif skip_until_end and line.startswith("---"):
                        skip_until_end = False
                        new_lines.append("")
                        new_lines.append(line)
                    elif not skip_until_end:
                        new_lines.append(line)

                return "\n".join(new_lines)
            else:
                return template_content

        except Exception as e:
            self.logger.warning(
                f"ハイブリッド生成中にエラーが発生しました: {e}。テンプレートのみを使用します。",
                exc_info=True,
            )
            return template_content

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

    def _generate_llm_setup_section(self) -> list[str]:
        """LLM環境セットアップセクションを生成"""
        lines = []
        lines.append("### LLM環境のセットアップ")
        lines.append("")

        llm_mode = self.agents_config.get("llm_mode", "both")
        api_config = self.agents_config.get("api")
        if api_config is None:
            api_config = {}
        local_config = self.agents_config.get("local")
        if local_config is None:
            local_config = {}

        if llm_mode in ["api", "both"]:
            lines.append("#### APIを使用する場合")
            lines.append("")

            lines.append("1. **APIキーの取得と設定**")
            lines.append("")

            api_provider = api_config.get("provider", "openai")
            api_key_env = api_config.get("api_key_env", "OPENAI_API_KEY")

            if api_provider == "openai":
                lines.append("   - OpenAI APIキーを取得: https://platform.openai.com/api-keys")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            elif api_provider == "anthropic":
                lines.append("   - Anthropic APIキーを取得: https://console.anthropic.com/")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            else:
                api_endpoint = api_config.get("endpoint", "")
                lines.append(f"   - カスタムAPIエンドポイントを使用: {api_endpoint}")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")

            lines.append("")
            lines.append("2. **API使用時の注意事項**")
            lines.append("   - APIレート制限に注意してください")
            lines.append("   - コスト管理のために使用量を監視してください")
            lines.append("")

        if llm_mode in ["local", "both"]:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")

            lines.append("1. **ローカルLLMのインストール**")
            lines.append("")

            local_provider = local_config.get("provider", "ollama")
            local_model = local_config.get("model", "llama3")
            # 一般的な手順としてlocalhostを使用
            local_base_url = "http://localhost:11434"

            if local_provider == "ollama":
                lines.append("   - Ollamaをインストール: https://ollama.ai/")
                lines.append(f"   - モデルをダウンロード: `ollama pull {local_model}`")
                lines.append("   - サービスを起動: `ollama serve`")
                lines.append(f"   - ベースURL: {local_base_url}")
            elif local_provider == "lmstudio":
                lines.append("   - LM Studioをインストール: https://lmstudio.ai/")
                lines.append("   - モデルをダウンロードして起動")
                lines.append(f"   - ベースURL: {local_base_url}")
            else:
                lines.append("   - カスタムローカルLLMを設定")
                lines.append(f"   - ベースURL: {local_base_url}")

            lines.append("")
            lines.append("2. **ローカルLLM使用時の注意事項**")
            lines.append("   - モデルが起動していることを確認してください")
            lines.append("   - ローカルリソース（メモリ、CPU）を監視してください")
            lines.append("")

        return lines

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
