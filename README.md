# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、プロジェクトのエージェントに関するドキュメントを自動生成・同期させる CLI ツールです。  
Python で実装されており、`pyproject.toml` の `scripts` セクションから

```
$ agents-docs-sync
```  

というコマンドが直接呼び出せます（同時に `agents_docs_sync` エイリアスも用意）。

## 技術スタック  
- **Python 3.10+**：メインロジック、データモデル。  
- **Shell スクリプト**：CLI のエントリポイントと環境設定を簡易化。  
- **pydantic / dataclasses（推定）**：構成ファイルのバリデーション。  
- **Jinja2 テンプレート**（想定）：Markdown 出力テンプレートとして使用。

## アーキテクチャ概要  

```
┌───────────────────────┐
│  CLI (agents-docs-sync) │   ← pyproject.toml のスクリプトエントリポイント  
├─────────────┬───────────┤
│ config-loader │ generator │   ← docgen/docgen.py 内の main() が実行  
├───────▼──────┴──────▲────┤
│  AgentsConfig (ProjectOverview, AgentsGenerationConfig, …)   │   
└─────────────────────────────┘
```

1. **CLI**：`argparse / click` によりオプション解析。 `--help`, `-v`, `--config <path>` 等をサポート。  
2. **構成読み込み**：指定された YAML/JSON ファイルから `AgentsConfig` を生成し、各セクション（ProjectOverview, AgentsGenerationConfig など）へマッピング。  
3. **ドキュメント生成**：テンプレートエンジンで `AGENTS.md` 等の Markdown を構築。  
4. **出力**：指定ディレクトリに書き込み、差分があれば上書き／ログを残す。

## 主な機能  

- **自動同期**：コードベースとドキュメントを常時一致させるためのワンライナー。  
- **構成ファイルでカスタマイズ可能**：プロジェクト概要、エージェント設定セクション、生成オプションなどを YAML 形式で記述できる。  
- **テンプレートベース出力**：Jinja2 テンプレートにより Markdown のフォーマット自由度が高い。  
- **CLI オプション**：`--dry-run`, `--verbose`, `--output <dir>` 等、開発フローをサポートする便利オプション群。  
- **テストとCI統合**：Release ドキュメント (`docs/RELEASE.md`) で示されるように `agents-docs-sync --help` が常時動作し、GitHub Actions 等の CI に組み込み可能。

## 実装ポイント  

| コンポーネント | 主な役割 |
|-----------------|----------|
| **docgen/models/agents.py** | データモデル (`ProjectOverview`, `AgentsConfigSection`, `AgentsGenerationConfig`, `AgentsDocument`) を定義し、構成ファイルのバリデーションを担当。 |
| **docgen/docgen.py** | CLI から呼び出されるエントリポイントで、ロード・検証・生成まで一連のフローを実行する。 |
| **templates/** | Markdown テンプレート群（例：`agents.md.j2`）。テンプレートによりセクションごとのレイアウトが決定。 |

## 使い方サンプル  

```bash
# リポジトリの取得と初期化
git clone https://github.com/your-org/agents-docs-sync.git
cd agents-docs-sync

# 必要な依存をインストール（例: pipenv, poetry）
pip install -e .

# 設定ファイルを書き換えて実行
cat <<EOF > config.yaml
project_overview:
  name: "My Agent Suite"
  description: |
    エージェントの概要と利用方法。
agents_generation_config:
  output_dir: docs/
...
EOF

agents-docs-sync --config config.yaml
```

## 今後の拡張予定  

- **プラグインシステム**：外部エージェント情報を取得する API プロバイダー統合。  
- **多言語対応**：テンプレートに i18n を導入し、複数言語でドキュメント生成可能に。  
- **Web UI**：設定ファイルのビジュアル編集とプレビュー機能を提供。

---

agents-docs-sync は、コード変更時に自動的に最新状態のエージェントドキュメントを作成し、開発者が手間なく情報共有できるよう設計されたツールです。  
技術的な詳細は `docgen` パッケージ内で完結しており、Python とシンプルな Shell スクリプトだけで導入・運用できます。





## 使用技術

- Shell
- Python

## 依存関係

- **Python**: `pyproject.toml` または `requirements.txt` を参照

## セットアップ


## 前提条件

- Python 3.12以上



## インストール


### Python

```bash
# uvを使用する場合
uv sync
```




## LLM環境のセットアップ

### APIを使用する場合

1. **APIキーの取得と設定**

   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください




## ビルドおよびテスト

### ビルド

```bash
uv sync
```
```bash
uv build
```
```bash
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest tests/ -v --tb=short
```
```bash
npm test
```
```bash
go test ./...
```





---

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 21:27:14*