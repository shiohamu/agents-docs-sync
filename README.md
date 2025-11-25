# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
agents-docs-sync は、コミットごとに自動でテスト実行・ドキュメント生成を行い、その結果を `AGENTS.md` に反映させる CI/CD パイプラインです。  
主な構成は次の通りです。

- **使用言語**：Python とシェルスクリプト
- **主要タスク**
  - Python テスト（pytest + pytest‑cov）を実行し、コードカバレッジを確認
  - `docgen/docgen.py` を走らせて API ドキュメントとサンプルリファレンスを生成  
    (`uv run python3 docgen/docgen.py`)
  - 自動更新されたドキュメント内容で `AGENTS.md` を再構築し、コミットに含める
- **依存関係**（Python）
  ```toml
  pyyaml>=6.0.3
  pytest>=7.4.0
  pytest-cov>=4.1.0
  pytest-mock>=3.11.1
  ```
- **ビルド手順**
  1. `uv sync` – 依存関係の同期  
  2. `uv build` – ビルド（必要に応じて）  
  3. `uv run python3 docgen/docgen.py`
- **テスト実行**  
  - Python: `uv run pytest tests/ -v --tb=short`  
  - JavaScript (npm): `npm test`  
  - Go: `go test ./...`
- **コーディング規約**：リントツールとして Ruff を使用し、コード品質を維持

このプロジェクトにより、コミット時点で常に最新のテスト結果とドキュメントが生成されるため、開発者は一貫した情報を迅速に確認できます。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 00:15:45*