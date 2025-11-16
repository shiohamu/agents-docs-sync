"""
AGENTS.md生成モジュール（OpenAI仕様準拠）
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# 相対インポートを使用（.docgenがパッケージとして認識される場合）
# フォールバック: 絶対インポート
try:
    from ..collectors.project_info_collector import ProjectInfoCollector
    from ..utils.logger import get_logger
except ImportError:
    # 相対インポートが失敗した場合のフォールバック
    import sys
    DOCGEN_DIR = Path(__file__).parent.parent.resolve()
    if str(DOCGEN_DIR) not in sys.path:
        sys.path.insert(0, str(DOCGEN_DIR))
    from collectors.project_info_collector import ProjectInfoCollector
    from utils.logger import get_logger

logger = get_logger("agents_generator")


class AgentsGenerator:
    """AGENTS.md生成クラス（OpenAI仕様準拠）"""

    def __init__(self, project_root: Path, languages: List[str], config: Dict[str, Any]):
        """
        初期化

        Args:
            project_root: プロジェクトのルートディレクトリ
            languages: 検出された言語のリスト
            config: 設定辞書
        """
        self.project_root = project_root
        self.languages = languages
        self.config = config
        self.output_path = Path(
            config.get('output', {}).get('agents_doc', 'AGENTS.md')
        )
        if not self.output_path.is_absolute():
            self.output_path = project_root / self.output_path

        # プロジェクト情報収集器
        self.collector = ProjectInfoCollector(project_root)

        # AGENTS設定
        self.agents_config = config.get('agents', {})

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
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)

            return True
        except Exception as e:
            logger.error(f"AGENTS.md生成に失敗しました: {e}", exc_info=True)
            return False

    def _generate_markdown(self, project_info: Dict[str, Any]) -> str:
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
        lines.append("このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。")
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
        custom_instructions = self.agents_config.get('custom_instructions')
        if custom_instructions:
            lines.extend(self._generate_custom_instructions_section(custom_instructions))
            lines.append("")
            lines.append("---")
            lines.append("")

        # フッター
        lines.append(f"*このドキュメントは自動生成されています。最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

        return '\n'.join(lines)

    def _generate_project_overview(self, project_info: Dict[str, Any]) -> List[str]:
        """プロジェクト概要セクションを生成"""
        lines = []
        lines.append("## プロジェクト概要")
        lines.append("")

        # READMEから説明を取得（簡易版）
        readme_path = self.project_root / 'README.md'
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding='utf-8')
            # 最初の段落を抽出（簡易版）
            for line in readme_content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    lines.append(line)
                    break

        lines.append("")
        lines.append(f"**使用技術**: {', '.join(self.languages) if self.languages else '不明'}")
        return lines

    def _generate_setup_section(self, project_info: Dict[str, Any]) -> List[str]:
        """開発環境セットアップセクションを生成"""
        lines = []
        lines.append("## 開発環境のセットアップ")
        lines.append("")

        # 前提条件
        lines.append("### 前提条件")
        lines.append("")
        lines.append("- Python 3.12以上")
        if 'javascript' in self.languages:
            lines.append("- Node.js 18以上")
        lines.append("")

        # 依存関係のインストール
        lines.append("### 依存関係のインストール")
        lines.append("")

        dependencies = project_info.get('dependencies', {})
        if 'python' in dependencies:
            lines.append("#### Python依存関係")
            lines.append("")
            lines.append("```bash")
            for dep_file in ['requirements.txt', 'requirements-docgen.txt', 'requirements-test.txt']:
                req_path = self.project_root / dep_file
                if req_path.exists():
                    lines.append(f"pip install -r {dep_file}")
            lines.append("```")
            lines.append("")

        if 'nodejs' in dependencies:
            lines.append("#### Node.js依存関係")
            lines.append("")
            lines.append("```bash")
            lines.append("npm install")
            lines.append("```")
            lines.append("")

        # LLM環境のセットアップ
        lines.extend(self._generate_llm_setup_section())

        return lines

    def _generate_llm_setup_section(self) -> List[str]:
        """LLM環境セットアップセクションを生成"""
        lines = []
        lines.append("### LLM環境のセットアップ")
        lines.append("")

        llm_mode = self.agents_config.get('llm_mode', 'both')
        api_config = self.agents_config.get('api', {})
        local_config = self.agents_config.get('local', {})

        if llm_mode in ['api', 'both']:
            lines.append("#### APIを使用する場合")
            lines.append("")
            lines.append("1. **APIキーの取得と設定**")
            lines.append("")

            api_provider = api_config.get('provider', 'openai')
            api_key_env = api_config.get('api_key_env', 'OPENAI_API_KEY')

            if api_provider == 'openai':
                lines.append("   - OpenAI APIキーを取得: https://platform.openai.com/api-keys")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            elif api_provider == 'anthropic':
                lines.append("   - Anthropic APIキーを取得: https://console.anthropic.com/")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")
            else:
                api_endpoint = api_config.get('endpoint', '')
                lines.append(f"   - カスタムAPIエンドポイントを使用: {api_endpoint}")
                lines.append(f"   - 環境変数に設定: `export {api_key_env}=your-api-key-here`")

            lines.append("")
            lines.append("2. **API使用時の注意事項**")
            lines.append("   - APIレート制限に注意してください")
            lines.append("   - コスト管理のために使用量を監視してください")
            lines.append("")

        if llm_mode in ['local', 'both']:
            lines.append("#### ローカルLLMを使用する場合")
            lines.append("")
            lines.append("1. **ローカルLLMのインストール**")
            lines.append("")

            local_provider = local_config.get('provider', 'ollama')
            local_model = local_config.get('model', 'llama3')
            local_base_url = local_config.get('base_url', 'http://localhost:11434')

            if local_provider == 'ollama':
                lines.append("   - Ollamaをインストール: https://ollama.ai/")
                lines.append(f"   - モデルをダウンロード: `ollama pull {local_model}`")
                lines.append("   - サービスを起動: `ollama serve`")
            elif local_provider == 'lmstudio':
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

    def _generate_build_test_section(self, project_info: Dict[str, Any]) -> List[str]:
        """ビルド/テストセクションを生成"""
        lines = []
        lines.append("## ビルドおよびテスト手順")
        lines.append("")

        # ビルド手順
        lines.append("### ビルド手順")
        lines.append("")
        build_commands = project_info.get('build_commands', [])
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
        test_commands = project_info.get('test_commands', [])
        if test_commands:
            llm_mode = self.agents_config.get('llm_mode', 'both')

            if llm_mode in ['api', 'both']:
                lines.append("#### APIを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")

            if llm_mode in ['local', 'both']:
                lines.append("#### ローカルLLMを使用する場合")
                lines.append("")
                lines.append("```bash")
                for cmd in test_commands:
                    lines.append(cmd)
                lines.append("```")
                lines.append("")
                lines.append("**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。")
                lines.append("")
        else:
            lines.append("テストコマンドは設定されていません。")
        lines.append("")

        return lines

    def _generate_coding_standards_section(self, project_info: Dict[str, Any]) -> List[str]:
        """コーディング規約セクションを生成"""
        lines = []
        lines.append("## コーディング規約")
        lines.append("")

        coding_standards = project_info.get('coding_standards', {})

        if coding_standards:
            # フォーマッター
            formatter = coding_standards.get('formatter')
            if formatter:
                lines.append("### フォーマッター")
                lines.append("")
                lines.append(f"- **{formatter}** を使用")
                if formatter == 'black':
                    lines.append("  ```bash")
                    lines.append("  black .")
                    lines.append("  ```")
                elif formatter == 'prettier':
                    lines.append("  ```bash")
                    lines.append("  npx prettier --write .")
                    lines.append("  ```")
                lines.append("")

            # リンター
            linter = coding_standards.get('linter')
            if linter:
                lines.append("### リンター")
                lines.append("")
                lines.append(f"- **{linter}** を使用")
                if linter == 'ruff':
                    lines.append("  ```bash")
                    lines.append("  ruff check .")
                    lines.append("  ruff format .")
                    lines.append("  ```")
                lines.append("")

            # スタイルガイド
            style_guide = coding_standards.get('style_guide')
            if style_guide:
                lines.append("### スタイルガイド")
                lines.append("")
                lines.append(f"- {style_guide} に準拠")
                lines.append("")
        else:
            lines.append("コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。")
            lines.append("")

        return lines

    def _generate_pr_section(self, project_info: Dict[str, Any]) -> List[str]:
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
        test_commands = project_info.get('test_commands', [])
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

    def _generate_custom_instructions_section(self, custom_instructions: str) -> List[str]:
        """カスタム指示セクションを生成"""
        lines = []
        lines.append("## プロジェクト固有の指示")
        lines.append("")
        lines.append(custom_instructions)
        lines.append("")
        return lines
