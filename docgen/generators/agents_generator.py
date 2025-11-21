"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
Outlines統合で構造化出力を実現
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import BaseModel, Field
else:
    try:
        from pydantic import BaseModel, Field

        PYDANTIC_AVAILABLE = True
    except ImportError:
        PYDANTIC_AVAILABLE = False

        # Fallback for when pydantic is not available
        class BaseModel:
            pass

        def Field(**kwargs):
            return None


# 相対インポートを使用（docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
try:
    from ..collectors.project_info_collector import ProjectInfoCollector
    from ..utils.llm_client import LLMClientFactory
    from ..utils.logger import get_logger
    from ..utils.outlines_utils import (
        clean_llm_output,
        create_outlines_model,
        should_use_outlines,
        validate_output,
    )
except ImportError:
    # 相対インポートが失敗した場合のフォールバック
    import sys

    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from collectors.project_info_collector import ProjectInfoCollector
    from utils.llm_client import LLMClientFactory
    from utils.logger import get_logger
    from utils.outlines_utils import (
        clean_llm_output,
        create_outlines_model,
        should_use_outlines,
        validate_output,
    )

logger = get_logger("agents_generator")


class AgentsDocument(BaseModel):
    """AGENTS.mdドキュメントの構造化データモデル"""

    title: str = Field(description="ドキュメントのタイトル")
    description: str = Field(description="プロジェクトの説明")
    project_overview: dict[str, Any] = Field(description="プロジェクト概要情報")
    setup_instructions: dict[str, Any] = Field(description="セットアップ手順")
    build_test_instructions: dict[str, Any] = Field(description="ビルド/テスト手順")
    coding_standards: dict[str, Any] = Field(description="コーディング規約")
    pr_guidelines: dict[str, Any] = Field(description="プルリクエスト手順")
    auto_generated_note: str = Field(description="自動生成に関する注意書き")


class AgentsGenerator:
    """AGENTS.md生成クラス（OpenAI仕様準拠）"""

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
        self.output_path: Path = Path(config.get("output", {}).get("agents_doc", "AGENTS.md"))
        if not self.output_path.is_absolute():
            self.output_path = project_root / self.output_path

        # プロジェクト情報収集器
        self.collector: ProjectInfoCollector = ProjectInfoCollector(project_root, package_managers)

        # AGENTS設定
        self.agents_config: dict[str, Any] = config.get("agents", {})

    def generate(self) -> bool:
        """
        AGENTS.mdを生成

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

            # ファイルに書き込み
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            return True
        except Exception as e:
            logger.error(f"AGENTS.md生成に失敗しました: {e}", exc_info=True)
            return False

    def _generate_markdown(self, project_info: dict[str, Any]) -> str:
        """
        プロジェクト情報からマークダウンを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        # 生成モードを取得（デフォルトは'template'）
        generation_config = self.agents_config.get("generation", {})
        mode = generation_config.get("agents_mode", "template")

        if mode == "llm":
            # LLM完全生成
            return self._generate_with_llm(project_info)
        elif mode == "hybrid":
            # ハイブリッド生成
            return self._generate_hybrid(project_info)
        else:
            # テンプレート生成（デフォルト）
            return self._generate_template(project_info)

    def _generate_template(self, project_info: dict[str, Any]) -> str:
        """
        テンプレートベースでマークダウンを生成（既存の実装）

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        lines = []

        # ヘッダー
        lines.append("# AGENTS ドキュメント")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(
            "このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # プロジェクト概要
        lines.extend(self._generate_project_overview(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # 開発環境のセットアップ
        lines.extend(self._generate_setup_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # ビルドおよびテスト手順
        lines.extend(self._generate_build_test_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # コーディング規約
        lines.extend(self._generate_coding_standards_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # プルリクエストの手順
        lines.extend(self._generate_pr_section(project_info))
        lines.append("")
        lines.append("---")
        lines.append("")

        # カスタム指示
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            lines.extend(self._generate_custom_instructions_section(custom_instructions))
            lines.append("")
            lines.append("---")
            lines.append("")

        # フッター
        lines.append(
            f"*このドキュメントは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )
        lines.append("")

        return "\n".join(lines)

    def _generate_with_llm(self, project_info: dict[str, Any]) -> str:
        """
        LLMを使用してAGENTS.mdを生成（Outlinesで構造化出力）

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
            logger.error(
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

    def _generate_with_outlines(self, project_info: dict[str, Any]) -> str:
        """
        Outlinesを使用して構造化されたAGENTS.mdを生成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            マークダウンの文字列
        """
        try:
            # LLMクライアントを取得
            client = self._get_llm_client_with_fallback()

            if not client:
                logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # Outlinesモデルを作成
            outlines_model = self._create_outlines_model(client)

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info)

            # 構造化出力モデルで生成
            logger.info("Outlinesを使用して構造化されたAGENTS.mdを生成中...")
            structured_data = outlines_model(prompt, AgentsDocument)

            # 構造化データをマークダウンに変換
            markdown = self._convert_structured_data_to_markdown(structured_data, project_info)

            return markdown

        except Exception as e:
            logger.error(
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
        return create_outlines_model(client)

    def _generate_with_llm_legacy(self, project_info: dict[str, Any]) -> str:
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
                logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレート生成にフォールバックします。"
                )
                return self._generate_template(project_info)

            # プロンプトを作成
            prompt = self._create_llm_prompt(project_info)

            # システムプロンプト
            system_prompt = """あなたは技術ドキュメント作成の専門家です。
AIコーディングエージェントがプロジェクトで効果的に作業するためのAGENTS.mdドキュメントを生成してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

            # LLMで生成
            logger.info("LLMを使用してAGENTS.mdを生成中...")
            generated_text = client.generate(prompt, system_prompt=system_prompt)

            if generated_text:
                # LLM出力をクリーンアップ
                cleaned_text = clean_llm_output(generated_text)

                # 出力を検証
                if not validate_output(cleaned_text):
                    logger.warning(
                        "LLM出力の検証に失敗しました。テンプレート生成にフォールバックします。"
                    )
                    return self._generate_template(project_info)

                # 生成されたテキストにタイムスタンプを追加
                lines = cleaned_text.split("\n")
                # フッターを追加（既に含まれていない場合）
                if not any("自動生成されています" in line for line in lines):
                    lines.append("")
                    lines.append(
                        f"*このドキュメントは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
                    )
                return "\n".join(lines)
            else:
                logger.warning("LLM生成が空でした。テンプレート生成にフォールバックします。")
                return self._generate_template(project_info)

        except Exception as e:
            logger.error(
                f"LLM生成中にエラーが発生しました: {e}。テンプレート生成にフォールバックします。",
                exc_info=True,
            )
            return self._generate_template(project_info)

    def _generate_hybrid(self, project_info: dict[str, Any]) -> str:
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
                logger.warning(
                    "LLMクライアントの作成に失敗しました。テンプレートのみを使用します。"
                )
                return template_content

            # プロジェクト概要セクションのみLLMで改善
            prompt = f"""以下のプロジェクト情報を基に、AGENTS.mdの「プロジェクト概要」セクションを改善してください。
既存のテンプレート生成内容を参考に、より詳細で有用な説明を生成してください。

プロジェクト情報:
{self._format_project_info_for_prompt(project_info)}

既存のテンプレート生成内容:
{self._generate_project_overview(project_info)}

改善された「プロジェクト概要」セクションをマークダウン形式で出力してください。
重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
手動セクション（<!-- MANUAL_START:description --> と <!-- MANUAL_END:description -->）は保持してください。"""

            system_prompt = """あなたは技術ドキュメント作成の専門家です。プロジェクト概要を明確で有用な形で記述してください。
最終的な出力のみを生成し、思考過程や試行錯誤の痕跡を含めないでください。"""

            logger.info("LLMを使用してプロジェクト概要セクションを改善中...")
            improved_overview = client.generate(prompt, system_prompt=system_prompt)

            if improved_overview:
                # LLM出力をクリーンアップ
                cleaned_overview = clean_llm_output(improved_overview)

                # 出力を検証
                if not validate_output(cleaned_overview):
                    logger.warning("LLM出力の検証に失敗しました。テンプレートのみを使用します。")
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
            logger.warning(
                f"ハイブリッド生成中にエラーが発生しました: {e}。テンプレートのみを使用します。",
                exc_info=True,
            )
            return template_content

    def _create_llm_prompt(self, project_info: dict[str, Any]) -> str:
        """
        LLM用のプロンプトを作成

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            プロンプト文字列
        """
        prompt = f"""以下のプロジェクト情報を基に、AIコーディングエージェント向けのAGENTS.mdドキュメントを生成してください。

{self._format_project_info_for_prompt(project_info)}

以下のセクションを含めてください:
1. プロジェクト概要（使用技術を含む）
2. 開発環境のセットアップ（前提条件、依存関係のインストール、LLM環境のセットアップ）
3. ビルドおよびテスト手順
4. コーディング規約
5. プルリクエストの手順

重要: 最終的な出力のみを生成してください。思考過程、試行錯誤の痕跡、メタ的な説明は一切含めないでください。
マークダウン形式で、構造化された明確なドキュメントを作成してください。
手動セクション（<!-- MANUAL_START:... --> と <!-- MANUAL_END:... -->）は保持してください。"""

        return prompt

    def _format_project_info_for_prompt(self, project_info: dict[str, Any]) -> str:
        """
        プロジェクト情報をプロンプト用にフォーマット

        Args:
            project_info: プロジェクト情報の辞書

        Returns:
            フォーマットされた文字列
        """
        lines = []
        lines.append(f"プロジェクト名: {self.project_root.name}")
        lines.append(f"使用言語: {', '.join(self.languages) if self.languages else '不明'}")

        description = project_info.get("description")
        if description:
            lines.append(f"説明: {description}")

        dependencies = project_info.get("dependencies", {})
        if dependencies:
            lines.append("依存関係:")
            for dep_type, deps in dependencies.items():
                lines.append(f"  - {dep_type}: {', '.join(deps[:10])}")

        build_commands = project_info.get("build_commands", [])
        if build_commands:
            lines.append("ビルドコマンド:")
            for cmd in build_commands:
                lines.append(f"  - {cmd}")

        test_commands = project_info.get("test_commands", [])
        if test_commands:
            lines.append("テストコマンド:")
            for cmd in test_commands:
                lines.append(f"  - {cmd}")

        coding_standards = project_info.get("coding_standards", {})
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

    def _generate_project_overview(self, project_info: dict[str, Any]) -> list[str]:
        """プロジェクト概要セクションを生成"""
        lines = []
        lines.append("## プロジェクト概要")
        lines.append("")

        lines.append("<!-- MANUAL_START:description -->")
        lines.append("")

        # プロジェクト情報から説明を取得
        description = project_info.get("description")
        if description:
            lines.append(description)
        else:
            # READMEから説明を取得（フォールバック）
            readme_path = self.project_root / "README.md"
            if readme_path.exists():
                readme_content = readme_path.read_text(encoding="utf-8")
                # 最初の段落を抽出（簡易版）
                for line in readme_content.split("\n"):
                    line_stripped = line.strip()
                    if (
                        line_stripped
                        and not line_stripped.startswith("#")
                        and not line_stripped.startswith("<!--")
                    ):
                        # 汎用的なテンプレート文をスキップ
                        if "このプロジェクトの説明をここに記述してください" not in line_stripped:
                            lines.append(line)
                            break

        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        lines.append("")
        lines.append("<!-- MANUAL_END:description -->")
        return lines

    def _generate_setup_section(self, project_info: dict[str, Any]) -> list[str]:
        """開発環境セットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        lines.append("### 前提条件")
        lines.append("")
        lines.append("- Python 3.12以上")
        if "javascript" in self.languages:
            lines.append("- Node.js 18以上")
        lines.append("")

        # 依存関係のインストール
        lines.append("### 依存関係のインストール")
        lines.append("")

        dependencies = project_info.get("dependencies", {})

        # Python依存関係
        if "python" in self.languages:
            pm = self.package_managers.get("python", "pip")
            lines.append("#### Python依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "uv":
                lines.append("uv sync")
            elif pm == "poetry":
                lines.append("poetry install")
            elif pm == "conda":
                lines.append("conda env create -f environment.yml")
            else:  # pip
                for dep_file in [
                    "requirements.txt",
                    "requirements-docgen.txt",
                    "requirements-test.txt",
                ]:
                    req_path = self.project_root / dep_file
                    if req_path.exists():
                        lines.append(f"pip install -r {dep_file}")
            lines.append("```")
            lines.append("")

        # JavaScript/TypeScript依存関係
        if "javascript" in self.languages or "typescript" in self.languages:
            pm = self.package_managers.get("javascript", "npm")
            lang_name = "TypeScript" if "typescript" in self.languages else "JavaScript"
            lines.append(f"#### {lang_name}依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "pnpm":
                lines.append("pnpm install")
            elif pm == "yarn":
                lines.append("yarn install")
            else:  # npm
                lines.append("npm install")
            lines.append("```")
            lines.append("")

        # Go依存関係
        if "go" in self.languages:
            pm = self.package_managers.get("go", "go")
            lines.append("#### Go依存関係")
            lines.append("")
            lines.append("```bash")
            if pm == "dep":
                lines.append("dep ensure")
            elif pm == "glide":
                lines.append("glide install")
            else:  # go modules
                lines.append("go mod download")
            lines.append("```")
            lines.append("")

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_llm_setup_section(self) -> list[str]:
        """LLM環境セットアップセクションを生成"""
        lines = []
        lines.append("### LLM環境のセットアップ")
        lines.append("")

        llm_mode = self.agents_config.get("llm_mode", "both")
        api_config = self.agents_config.get("api", {})
        local_config = self.agents_config.get("local", {})

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
            local_base_url = local_config.get("base_url", "http://localhost:11434")

            if local_provider == "ollama":
                lines.append("   - Ollamaをインストール: https://ollama.ai/")
                lines.append(f"   - モデルをダウンロード: `ollama pull {local_model}`")
                lines.append("   - サービスを起動: `ollama serve`")
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

    def _generate_build_test_section(self, project_info: dict[str, Any]) -> list[str]:
        """ビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")

        # ビルド手順
        lines.append("### ビルド手順")
        lines.append("")
        build_commands = project_info.get("build_commands", [])
        if build_commands:
            lines.append("```bash")
            for cmd in build_commands:
                lines.append(cmd)
            lines.append("```")
        else:
            lines.append("ビルド手順は設定されていません。")
        lines.append("")

        # テスト実行
        lines.append("### テスト実行")
        lines.append("")
        test_commands = project_info.get("test_commands", [])
        if test_commands:
            llm_mode = self.agents_config.get("llm_mode", "both")

            if llm_mode in ["api", "both"]:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")

        return lines

    def _generate_coding_standards_section(self, project_info: dict[str, Any]) -> list[str]:
        """コーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        coding_standards = project_info.get("coding_standards", {})

        if coding_standards:
            # フォーマッター
            formatter = coding_standards.get("formatter")
            if formatter:
                lines.append("### フォーマッター")
                lines.append("")
                lines.append(f"- **{formatter}** を使用")
                if formatter == "black":
                    lines.append("  ```bash")
                    lines.append("  black .")
                    lines.append("  ```")
                elif formatter == "prettier":
                    lines.append("  ```bash")
                    lines.append("  npx prettier --write .")
                    lines.append("  ```")
                lines.append("")

            # リンター
            linter = coding_standards.get("linter")
            if linter:
                lines.append("### リンター")
                lines.append("")
                lines.append(f"- **{linter}** を使用")
                if linter == "ruff":
                    lines.append("  ```bash")
                    lines.append("  ruff check .")
                    lines.append("  ruff format .")
                    lines.append("  ```")
                lines.append("")

            # スタイルガイド
            style_guide = coding_standards.get("style_guide")
            if style_guide:
                lines.append("### スタイルガイド")
                lines.append("")
                lines.append(f"- {style_guide} に準拠")
                lines.append("")
        else:
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_pr_section(self, project_info: dict[str, Any]) -> list[str]:
        """プルリクエストセクションを生成"""
        lines = []
        lines.append("## プルリクエストの手順")
        lines.append("")
        lines.append("1. **ブランチの作成**")
        lines.append("   ```bash")
        lines.append("   git checkout -b feature/your-feature-name")
        lines.append("   ```")
        lines.append("")
        lines.append("2. **変更のコミット**")
        lines.append("   - コミットメッセージは明確で説明的に")
        lines.append("   - 関連するIssue番号を含める")
        lines.append("")
        lines.append("3. **テストの実行**")
        lines.append("   ```bash")
        test_commands = project_info.get("test_commands", [])
        for cmd in test_commands:
            lines.append(f"   {cmd}")
        if not test_commands:
            lines.append("   # テストコマンドを実行")
        lines.append("   ```")
        lines.append("")
        lines.append("4. **プルリクエストの作成**")
        lines.append("   - タイトル: `[種類] 簡潔な説明`")
        lines.append("   - 説明: 変更内容、テスト結果、関連Issueを記載")
        lines.append("")

        return lines

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

    def _convert_structured_data_to_markdown(
        self, data: AgentsDocument, project_info: dict[str, Any]
    ) -> str:
        """
        構造化データをマークダウン形式に変換

        Args:
            data: 構造化されたAGENTSドキュメントデータ
            project_info: プロジェクト情報

        Returns:
            マークダウン形式の文字列
        """
        lines = []

        # ヘッダー
        lines.append(f"# {data.title}")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(
            "このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # プロジェクト概要
        lines.append("## プロジェクト概要")
        lines.append("")
        lines.append("<!-- MANUAL_START:description -->")
        lines.append("")
        lines.append(data.description)
        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        lines.append("")
        lines.append("<!-- MANUAL_END:description -->")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 開発環境のセットアップ
        lines.extend(self._generate_setup_section_from_structured(data.setup_instructions))
        lines.append("")
        lines.append("---")
        lines.append("")

        # ビルドおよびテスト手順
        lines.extend(
            self._generate_build_test_section_from_structured(data.build_test_instructions)
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # コーディング規約
        lines.extend(self._generate_coding_standards_from_structured(data.coding_standards))
        lines.append("")
        lines.append("---")
        lines.append("")

        # プルリクエストの手順
        lines.extend(self._generate_pr_section_from_structured(data.pr_guidelines))
        lines.append("")
        lines.append("---")
        lines.append("")

        # カスタム指示
        custom_instructions = self.agents_config.get("custom_instructions")
        if custom_instructions:
            lines.extend(self._generate_custom_instructions_section(custom_instructions))
            lines.append("")
            lines.append("---")
            lines.append("")

        # フッター
        lines.append(data.auto_generated_note)
        lines.append("")

        return "\n".join(lines)

    def _generate_setup_section_from_structured(self, setup_data: dict[str, Any]) -> list[str]:
        """構造化データからセットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        prerequisites = setup_data.get("prerequisites", [])
        if prerequisites:
            lines.append("### 前提条件")
            lines.append("")
            for prereq in prerequisites:
                lines.append(f"- {prereq}")
            lines.append("")

        # 依存関係のインストール
        installation_steps = setup_data.get("installation_steps", [])
        if installation_steps:
            lines.append("### 依存関係のインストール")
            lines.append("")
            lines.append("```bash")
            for step in installation_steps:
                lines.append(step)
            lines.append("```")
            lines.append("")

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_build_test_section_from_structured(
        self, build_test_data: dict[str, Any]
    ) -> list[str]:
        """構造化データからビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")

        # ビルド手順
        build_commands = build_test_data.get("build_commands", [])
        if build_commands:
            lines.append("### ビルド手順")
            lines.append("")
            lines.append("```bash")
            for cmd in build_commands:
                # uvプロジェクトの場合はpythonコマンドにuv runをつける
                display_cmd = cmd
                if "python" in self.package_managers and self.package_managers["python"] == "uv":
                    if cmd.startswith("python") and not cmd.startswith("uv run"):
                        display_cmd = f"uv run {cmd}"
                lines.append(display_cmd)
            lines.append("```")
        else:
            lines.append("ビルド手順は設定されていません。")
        lines.append("")

        # テスト実行
        test_commands = build_test_data.get("test_commands", [])
        if test_commands:
            lines.append("### テスト実行")
            lines.append("")
            llm_mode = self.agents_config.get("llm_mode", "both")

            if llm_mode in ["api", "both"]:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    display_cmd = cmd
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if (
                            cmd.startswith("python") or cmd.startswith("pytest")
                        ) and not cmd.startswith("uv run"):
                            display_cmd = f"uv run {cmd}"
                    lines.append(display_cmd)
                lines.append("```")
                lines.append("")

            if llm_mode in ["local", "both"]:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    # uvプロジェクトの場合はpythonコマンドにuv runをつける
                    display_cmd = cmd
                    if (
                        "python" in self.package_managers
                        and self.package_managers["python"] == "uv"
                    ):
                        if (
                            cmd.startswith("python") or cmd.startswith("pytest")
                        ) and not cmd.startswith("uv run"):
                            display_cmd = f"uv run {cmd}"
                    lines.append(display_cmd)
                lines.append("```")
                lines.append("")
                lines.append(
                    "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
                )
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")

        return lines

    def _generate_coding_standards_from_structured(
        self, standards_data: dict[str, Any]
    ) -> list[str]:
        """構造化データからコーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        standards = standards_data.get("standards", [])
        if standards:
            for standard in standards:
                lines.append(f"- {standard}")
            lines.append("")
        else:
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_pr_section_from_structured(self, pr_data: dict[str, Any]) -> list[str]:
        """構造化データからプルリクエストセクションを生成"""
        lines = []
        lines.append("## プルリクエストの手順")
        lines.append("")

        branch_creation = pr_data.get("branch_creation", "ブランチを作成")
        lines.append("1. **ブランチの作成**")
        lines.append(f"   {branch_creation}")
        lines.append("")

        commit_guidelines = pr_data.get("commit_guidelines", "コミットメッセージは明確で説明的に")
        lines.append("2. **変更のコミット**")
        lines.append(f"   - {commit_guidelines}")
        lines.append("")

        lines.append("3. **テストの実行**")
        lines.append("   ```bash")
        lines.append("   # テストコマンドを実行")
        lines.append("   ```")
        lines.append("")

        pr_creation = pr_data.get("pr_creation", "プルリクエストを作成")
        lines.append("4. **プルリクエストの作成**")
        lines.append(f"   - {pr_creation}")
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
        if not text:
            return text

        lines = text.split("\n")
        cleaned_lines = []
        in_code_block = False
        code_block_lang = None

        i = 0
        while i < len(lines):
            line = lines[i]

            # コードブロックの開始/終了を検出
            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip().lower()
                    # マークダウンコードブロック内の思考過程をスキップ
                    if "markdown" in code_block_lang:
                        i += 1
                        # 次の```までスキップ
                        while i < len(lines) and not lines[i].strip().startswith("```"):
                            i += 1
                        if i < len(lines):
                            i += 1  # ```をスキップ
                        in_code_block = False
                        continue
                    else:
                        cleaned_lines.append(line)
                        i += 1
                        continue
                else:
                    in_code_block = False
                    code_block_lang = None
                    cleaned_lines.append(line)
                    i += 1
                    continue

            # コードブロック内はそのまま保持
            if in_code_block:
                cleaned_lines.append(line)
                i += 1
                continue

            # 思考過程のパターンを検出
            line_lower = line.lower().strip()

            # 特殊なマーカーパターン（最初にチェック）
            if (
                "<|channel|>" in line
                or "<|message|>" in line
                or "commentary/analysis" in line_lower
            ):
                i += 1
                # 次の空行または通常のコンテンツまでスキップ
                while (
                    i < len(lines)
                    and not lines[i].strip().startswith("##")
                    and not lines[i].strip().startswith("<!--")
                ):
                    if lines[i].strip() and not any(
                        pattern in lines[i].lower()
                        for pattern in ["let's", "we need", "but we", "thus final"]
                    ):
                        break
                    i += 1
                continue

            # 思考過程の開始パターン
            thinking_patterns = [
                "we need to",
                "thus final answer",
                "let's generate",
                "let's do",
                "but we need",
                "hence final answer",
                "thus final output",
                "i will produce",
                "i think",
                "ok i'll",
                "let's finalize",
                "but i think",
                "but we need to",
                "thus final answer will",
                "we should produce",
                "we will output",
                "we must produce",
                "thus the final",
                "but the actual",
                "so i will",
                "i'm going to",
                "i'm still not sure",
                "but it's enough",
                "let's output",
                "let's produce",
                "let's final answer",
                "but we need the final",
                "thus final answer is",
                "we now produce",
                "this content includes",
                "but we also mention",
                "ok, i will",
                "thus we must",
                "but we need to ensure",
                "let's generate:",
                "we should produce final",
                "thus final answer will be",
                "but i'm still not sure",
                "but i think it's",
                "let's finalize:",
                "we need the final answer",
                "thus final answer:",
                "ok i'll produce",
                "以下が、",
                "改訂版です",
                "手動セクションは保持",
                "we should now",
                "we will not include",
                "should we keep",
                "possibly they want",
                "but we must keep",
                "but we might need",
                "however, user wrote",
                "also note",
                "but the user",
                "ok final output",
                "ok. i'll generate",
                "let's create final output",
                "check that it doesn't",
                "now i will provide",
                "the user wants",
                "they gave",
                "so we should",
                "so we can",
                "also keep",
                "we must not include",
                "so final output",
                "but we must also keep",
                "we must only output",
                "but we must",
            ]

            # 思考過程の行をスキップ
            if any(pattern in line_lower for pattern in thinking_patterns):
                i += 1
                continue

            # プレースホルダーや不完全な記述を検出
            placeholder_patterns = [
                "???",
                "(??)",
                "... ...",
                "|  | |",
                "---‐‐‐",
                "continue",
                "we should now",
                "this content, while present",
                "# ... (continue)",
            ]

            if any(pattern in line_lower for pattern in placeholder_patterns):
                i += 1
                continue

            # 空行の連続を制限（3行以上は2行に）
            if not line.strip():
                if cleaned_lines and not cleaned_lines[-1].strip():
                    if len(cleaned_lines) >= 2 and not cleaned_lines[-2].strip():
                        i += 1
                        continue

            cleaned_lines.append(line)
            i += 1

        # 結果を結合
        result = "\n".join(cleaned_lines)

        # 先頭と末尾の空行を削除
        result = result.strip()

        # 重複した説明を削除（同じ行が3回以上続く場合）
        lines_result = result.split("\n")
        deduplicated = []
        prev_line = None
        repeat_count = 0

        for line in lines_result:
            if line == prev_line:
                repeat_count += 1
                if repeat_count < 3:
                    deduplicated.append(line)
            else:
                repeat_count = 0
                deduplicated.append(line)
            prev_line = line

        return "\n".join(deduplicated)

    def _validate_output(self, text: str) -> bool:
        """
        LLMの出力を検証して、不適切な内容が含まれていないかチェック

        Args:
            text: 検証するテキスト

        Returns:
            検証に合格したかどうか
        """
        if not text or not text.strip():
            return False

        text_lower = text.lower()

        # 特殊なマーカーパターンをチェック
        if "<|channel|>" in text or "<|message|>" in text or "commentary/analysis" in text_lower:
            logger.warning("特殊なマーカーパターンが検出されました")
            return False

        # 思考過程のパターンが含まれていないかチェック
        thinking_patterns = [
            "thus final answer",
            "let's generate",
            "but we need",
            "i will produce",
            "i think",
            "let's finalize",
            "we should produce",
            "we will output",
            "thus the final",
            "i'm going to",
            "let's output",
            "let's produce",
            "but i think it's",
            "thus final answer will be",
            "以下が、",
            "改訂版です",
            "we should now",
            "we will not include",
            "should we keep",
            "possibly they want",
            "but we must keep",
            "but we might need",
            "however, user wrote",
            "also note",
            "but the user",
            "ok final output",
            "ok. i'll generate",
            "let's create final output",
            "check that it doesn't",
            "now i will provide",
            "the user wants",
            "they gave",
            "so we should",
            "so we can",
            "also keep",
            "we must not include",
            "so final output",
            "but we must also keep",
            "we must only output",
            "but we must",
        ]

        for pattern in thinking_patterns:
            if pattern in text_lower:
                logger.warning(f"思考過程のパターンが検出されました: {pattern}")
                return False

        # プレースホルダーが含まれていないかチェック
        placeholder_patterns = [
            "???",
            "(??)",
            "... ...",
            "|  | |",
            "---‐‐‐",
            "# ... (continue)",
        ]

        for pattern in placeholder_patterns:
            if pattern in text:
                logger.warning(f"プレースホルダーが検出されました: {pattern}")
                return False

        # マークダウンコードブロック内に思考過程が含まれていないかチェック
        lines = text.split("\n")
        in_markdown_block = False
        for line in lines:
            if line.strip().startswith("```"):
                lang = line.strip()[3:].strip().lower()
                if "markdown" in lang:
                    in_markdown_block = True
                elif in_markdown_block:
                    in_markdown_block = False
            elif in_markdown_block:
                if any(pattern in line.lower() for pattern in thinking_patterns):
                    logger.warning("マークダウンコードブロック内に思考過程が検出されました")
                    return False

        return True
