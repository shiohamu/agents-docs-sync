# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
`agents‑docs‐sync`は、コミットごとに自動でテストを実行し、ドキュメントを生成して `AGENTS.md` を更新するパイプラインです。  
主な構成要素は以下の通りです。

- **使用言語**：Python とシェルスクリプト
- **主要機能**
  - コミット時にテスト（pytest、npm test、go test）を実行し失敗したらビルド停止  
  - 成功後 `docgen/docgen.py` を走らせて最新の API ドキュメントと `AGENTS.md` を自動生成
- **依存関係**（Python）
  ```text
  pyyaml>=6.0.3
  pytest>=7.4.0
  pytest-cov>=4.1.0
  pytest-mock>=3.11.1
  ```
- **ビルド手順**
  ```bash
  uv sync           # 必要なパッケージを同期（仮想環境作成・依存関係解決）
  uv build          # ビルドプロセスの実行
  uv run python3 docgen/docgen.py   # ドキュメント生成スクリプトの起動
  ```
- **テスト手順**
  ```bash
  uv run pytest tests/ -v --tb=short    # Python テスト（詳細出力）
  npm test                               # Node.js のユニット／統合テスト
  go test ./...                          # Go モジュール全体のテスト実行
  ```
- **コーディング規約**  
  - 静的解析・フォーマッティングは `ruff` を使用

このプロジェクトにより、リポジトリ内で最新状態を保つドキュメントと一貫した品質保証が自動化されます。
## 使用技術

- Python
- Shell

## 依存関係

### Python
- anthropic>=0.74.1
- httpx>=0.28.1
- jinja2>=3.1.0
- openai>=2.8.1
- outlines>=1.2.8
- pydantic>=2.0.0
- pytest>=9.0.1
- pyyaml>=6.0.3

## セットアップ

<!-- MANUAL_START:setup -->
# Setup


## Prerequisites

- Python 3.12以上



## Installation


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
<!-- MANUAL_END:setup -->
# Setup


## Prerequisites

- Python 3.12以上



## Installation


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
uv build
uv run python3 docgen/docgen.py
```


### テスト

```bash
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```





---

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 05:27:33*