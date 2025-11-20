# ステップ1: AGENTS.md生成モジュールの実装

## 目的

コードベースからエージェント情報を抽出してAGENTS.mdを生成するモジュールを作成します。

## 作業内容

### 1. `docgen/generators/agents_generator.py`を作成

既存の`APIGenerator`と`ReadmeGenerator`を参考に、以下の構造で実装します：

```python
"""
AGENTS.md生成モジュール
"""

from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .parsers.python_parser import PythonParser
from .parsers.js_parser import JSParser
from .parsers.generic_parser import GenericParser


class AgentsGenerator:
    """AGENTS.md生成クラス"""

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

    def generate(self) -> bool:
        """
        AGENTS.mdを生成

        Returns:
            成功したかどうか
        """
        try:
            # 出力ディレクトリを作成
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            # エージェント情報を収集
            agents = self._extract_agents()

            # マークダウンを生成
            markdown = self._generate_markdown(agents)

            # ファイルに書き込み
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)

            return True
        except Exception as e:
            print(f"エラー: AGENTS.md生成に失敗しました: {e}")
            return False

    def _extract_agents(self) -> List[Dict[str, Any]]:
        """
        コードベースからエージェント情報を抽出

        Returns:
            エージェント情報のリスト
        """
        agents = []
        parsers = self._get_parsers()

        for parser in parsers:
            apis = parser.parse_project()
            # エージェント関連のAPIをフィルタリング
            for api in apis:
                if self._is_agent(api):
                    agents.append(api)

        return agents

    def _is_agent(self, api: Dict[str, Any]) -> bool:
        """
        指定されたAPIがエージェントかどうかを判定

        Args:
            api: API情報の辞書

        Returns:
            エージェントの場合True
        """
        name_lower = api['name'].lower()
        docstring_lower = (api.get('docstring', '') or '').lower()

        # 名前またはdocstringに"agent"が含まれるか
        return 'agent' in name_lower or 'agent' in docstring_lower

    def _get_parsers(self) -> List:
        """
        言語に応じたパーサーのリストを取得

        Returns:
            パーサーのリスト
        """
        parsers = []

        for lang in self.languages:
            if lang == 'python':
                parsers.append(PythonParser(self.project_root))
            elif lang in ['javascript', 'typescript']:
                parsers.append(JSParser(self.project_root))
            else:
                parsers.append(GenericParser(self.project_root, language=lang))

        return parsers

    def _generate_markdown(self, agents: List[Dict[str, Any]]) -> str:
        """
        エージェント情報からマークダウンを生成

        Args:
            agents: エージェント情報のリスト

        Returns:
            マークダウンの文字列
        """
        lines = []

        # ヘッダー
        lines.append("# AGENTS ドキュメント")
        lines.append("")
        lines.append(f"自動生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("このドキュメントは、コードベースから自動的に抽出されたエージェント情報をまとめたものです。")
        lines.append("")
        lines.append("---")
        lines.append("")

        if not agents:
            lines.append("エージェントが見つかりませんでした。")
            return '\n'.join(lines)

        # エージェントごとに出力
        for agent in agents:
            lines.append(f"## {agent['name']}")
            lines.append("")
            lines.append(f"**型**: `{agent['type']}`")
            lines.append("")
            lines.append(f"**シグネチャ**:")
            lines.append("```")
            lines.append(agent['signature'])
            lines.append("```")
            lines.append("")

            if agent.get('docstring'):
                lines.append("**説明**:")
                lines.append("")
                docstring_lines = agent['docstring'].split('\n')
                for doc_line in docstring_lines:
                    lines.append(doc_line)
                lines.append("")
            else:
                lines.append("*説明なし*")
                lines.append("")

            lines.append(f"*定義場所: {agent['file']}:{agent['line']}*")
            lines.append("")
            lines.append("---")
            lines.append("")

        return '\n'.join(lines)
```

## 確認事項

- [ ] ファイルが正しく作成されているか
- [ ] 既存の`APIGenerator`と同じ構造になっているか
- [ ] エラーハンドリングが適切か
- [ ] インポート文が正しいか

## 次のステップ

このステップが完了したら、[ステップ2: 設定ファイルの拡張](./step2-config-extension.md)に進んでください。

