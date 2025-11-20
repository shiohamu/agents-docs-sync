"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
"""

from datetime import datetime
from pathlib import Path
from typing import Any

# 相対インポートを使用（docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
from ..base_generator import BaseGenerator
from ..collectors.project_info_collector import ProjectInfoCollector
from ..utils.logger import get_logger
from ..utils.uv_utils import detect_uv_usage, wrap_command_with_uv

logger = get_logger("agents_generator")


class AgentsGenerator(BaseGenerator):
    """AGENTS.md生成クラス（OpenAI仕様準拠）"""

    def __init__(self, project_root: Path, languages: list[str], config: dict[str, Any]):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
        """
        super().__init__(project_root, languages, config)
        self.output_path = Path(config.get("output", {}).get("agents_doc", "AGENTS.md"))
        if not self.output_path.is_absolute():
            self.output_path = project_root / self.output_path

        # プロジェクト情報収集器
        self.collector = ProjectInfoCollector(project_root)

        # AGENTS設定
        self.agents_config = config.get("agents", {})

    def _has_uv_config(self) -> bool:
        """pyproject.tomlにuv設定があるかを確認"""
        pyproject = self.project_root / "pyproject.toml"
        if not pyproject.exists():
            return False

        try:
            import tomllib

            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
                return "tool" in data and "uv" in data["tool"]
        except ImportError:
            # tomllibが利用できない場合、テキスト検索で確認
            try:
                with open(pyproject, encoding="utf-8") as f:
                    content = f.read()
                    return "[tool.uv]" in content
            except Exception:
                return False
        except Exception:
            return False

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
            logger.error(f"AGENTS.md生成中に予期しないエラーが発生しました: {e}", exc_info=True)
            return False

    def _generate_markdown(self, project_info: dict[str, Any]) -> str:
        """
        プロジェクト情報からマークダウンを生成

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

    def _generate_project_overview(self, project_info: dict[str, Any]) -> list[str]:
        """プロジェクト概要セクションを生成"""
        lines = []
        lines.append("## プロジェクト概要")
        lines.append("")

        # READMEから説明を取得（簡易版）
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            # 最初の段落を抽出（簡易版）
            for line in readme_content.split("\n"):
                if line.strip() and not line.strip().startswith("#"):
                    lines.append(line)
                    break

        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        return lines

    def _generate_setup_section(self, project_info: dict[str, Any]) -> list[str]:
        """開発環境セットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        lines.extend(self._generate_prerequisites_section())

        # 依存関係のインストール
        lines.extend(self._generate_dependencies_section(project_info))

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_prerequisites_section(self) -> list[str]:
        """前提条件セクションを生成"""
        lines = []
        lines.append("### 前提条件")
        lines.append("")
        lines.append("- Python 3.12以上")
        if "javascript" in self.languages:
            lines.append("- Node.js 18以上")
        lines.append("")
        return lines

    def _generate_dependencies_section(self, project_info: dict[str, Any]) -> list[str]:
        """依存関係インストールセクションを生成"""
        lines = []
        lines.append("### 依存関係のインストール")
        lines.append("")

        dependencies = project_info.get("dependencies", {})

        if "python" in dependencies:
            lines.extend(self._generate_python_dependencies())

        if "nodejs" in dependencies:
            lines.extend(self._generate_nodejs_dependencies())

        return lines

    def _generate_python_dependencies(self) -> list[str]:
        """Python依存関係セクションを生成"""
        lines = []
        lines.append("#### Python依存関係")
        lines.append("")
        lines.append("```bash")
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
        return lines

    def _generate_nodejs_dependencies(self) -> list[str]:
        """Node.js依存関係セクションを生成"""
        lines = []
        lines.append("#### Node.js依存関係")
        lines.append("")
        lines.append("```bash")
        lines.append("npm install")
        lines.append("```")
        lines.append("")
        return lines

    def _generate_llm_setup_section(self) -> list[str]:
        """LLM環境セットアップセクションを生成"""
        lines = []
        lines.append("### LLM環境のセットアップ")
        lines.append("")

        llm_mode = self.agents_config.get("llm_mode", "both")

        if llm_mode in ["api", "both"]:
            lines.extend(self._generate_api_setup_section())

        if llm_mode in ["local", "both"]:
            lines.extend(self._generate_local_setup_section())

        return lines

    def _generate_api_setup_section(self) -> list[str]:
        """APIセットアップセクションを生成"""
        lines = []
        lines.append("#### APIを使用する場合")
        lines.append("")
        lines.append("1. **APIキーの取得と設定**")
        lines.append("")

        api_config = self.agents_config.get("api", {})
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

        return lines

    def _generate_local_setup_section(self) -> list[str]:
        """ローカルLLMセットアップセクションを生成"""
        lines = []
        lines.append("#### ローカルLLMを使用する場合")
        lines.append("")
        lines.append("1. **ローカルLLMのインストール**")
        lines.append("")

        local_config = self.agents_config.get("local", {})
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

        # uvの使用を確認
        uses_uv = detect_uv_usage(self.project_root)

        # ビルド手順
        lines.extend(self._generate_build_section(project_info, uses_uv))

        # テスト実行
        lines.extend(self._generate_test_section(project_info, uses_uv))

        return lines

    def _generate_build_section(self, project_info: dict[str, Any], uses_uv: bool) -> list[str]:
        """ビルド手順セクションを生成"""
        lines = []
        lines.append("### ビルド手順")
        lines.append("")
        build_commands = project_info.get("build_commands", [])

        # uvを使用している場合はコマンドをuv runでラップ
        if uses_uv:
            build_commands = [wrap_command_with_uv(cmd) for cmd in build_commands]

        # ビルドコマンドがある場合は表示
        if build_commands:
            lines.append("```bash")
            for cmd in build_commands:
                lines.append(cmd)
            lines.append("```")
        else:
            lines.append("ビルドコマンドは設定されていません。")

        lines.append("")
        return lines

    def _generate_test_section(self, project_info: dict[str, Any], uses_uv: bool) -> list[str]:
        """テスト実行セクションを生成"""
        lines = []
        lines.append("### テスト実行")
        lines.append("")
        test_commands = project_info.get("test_commands", [])

        # uvを使用している場合はコマンドをuv runでラップ
        if uses_uv:
            test_commands = [wrap_command_with_uv(cmd) for cmd in test_commands]

        if test_commands:
            lines.extend(self._generate_test_commands_by_mode(test_commands))
        elif uses_uv:
            # uvを使用している場合のデフォルトテストコマンド
            lines.extend(self._generate_default_test_commands())
        else:
            lines.append("テストコマンドは設定されていません。")

        lines.append("")
        return lines

    def _generate_test_commands_by_mode(self, test_commands: list[str]) -> list[str]:
        """LLMモード別のテストコマンドを生成"""
        lines = []
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

        return lines

    def _generate_default_test_commands(self) -> list[str]:
        """デフォルトのテストコマンドを生成"""
        lines = []
        llm_mode = self.agents_config.get("llm_mode", "both")

        if llm_mode in ["api", "both"]:
            lines.append("#### APIを使用する場合")
            lines.append("")
            lines.append("```bash")
            lines.append("uv run pytest tests/ -v --tb=short")
            lines.append("```")
            lines.append("")

        if llm_mode in ["local", "both"]:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")
            lines.append("```bash")
            lines.append("uv run pytest tests/ -v --tb=short")
            lines.append("```")
            lines.append("")
            lines.append(
                "**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。"
            )
            lines.append("")

        return lines

    def _generate_coding_standards_section(self, project_info: dict[str, Any]) -> list[str]:
        """コーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        coding_standards = project_info.get("coding_standards", {})

        if coding_standards:
            lines.extend(self._generate_formatter_section(coding_standards))
            lines.extend(self._generate_linter_section(coding_standards))
            lines.extend(self._generate_style_guide_section(coding_standards))
        else:
            lines.append(
                "コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。"
            )
            lines.append("")

        return lines

    def _generate_formatter_section(self, coding_standards: dict[str, Any]) -> list[str]:
        """フォーマッターセクションを生成"""
        lines = []
        formatter = coding_standards.get("formatter")
        if formatter:
            lines.append("### フォーマッター")
            lines.append("")
            lines.append(f"- **{formatter}** を使用")
            lines.extend(self._get_formatter_commands(formatter))
            lines.append("")
        return lines

    def _generate_linter_section(self, coding_standards: dict[str, Any]) -> list[str]:
        """リンターセクションを生成"""
        lines = []
        linter = coding_standards.get("linter")
        if linter:
            lines.append("### リンター")
            lines.append("")
            lines.append(f"- **{linter}** を使用")
            lines.extend(self._get_linter_commands(linter))
            lines.append("")
        return lines

    def _generate_style_guide_section(self, coding_standards: dict[str, Any]) -> list[str]:
        """スタイルガイドセクションを生成"""
        lines = []
        style_guide = coding_standards.get("style_guide")
        if style_guide:
            lines.append("### スタイルガイド")
            lines.append("")
            lines.append(f"- {style_guide} に準拠")
            lines.append("")
        return lines

    def _get_formatter_commands(self, formatter: str) -> list[str]:
        """フォーマッターのコマンドを取得"""
        if formatter == "black":
            return ["  ```bash", "  black .", "  ```"]
        elif formatter == "prettier":
            return ["  ```bash", "  npx prettier --write .", "  ```"]
        return []

    def _get_linter_commands(self, linter: str) -> list[str]:
        """リンターのコマンドを取得"""
        if linter == "ruff":
            return ["  ```bash", "  ruff check .", "  ruff format .", "  ```"]
        return []

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

        # uvの使用を確認
        uses_uv = detect_uv_usage(self.project_root)

        # uvを使用している場合はコマンドをuv runでラップ
        if uses_uv:
            test_commands = [wrap_command_with_uv(cmd) for cmd in test_commands]

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

    def _generate_custom_instructions_section(self, custom_instructions: str) -> list[str]:
        """カスタム指示セクションを生成"""
        lines = []
        lines.append("## プロジェクト固有の指示")
        lines.append("")
        lines.append(custom_instructions)
        lines.append("")
        return lines
