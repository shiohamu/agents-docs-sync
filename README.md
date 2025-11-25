# agents-docs-sync

<!-- MANUAL_START:description -->
<!-- MANUAL_END:description -->
`agents-docs-sync` は、コードベースに対するコミットごとに自動で以下を実行し、ドキュメントの整合性を保つパイプラインです。  

1. **テスト実行** – Python の `pytest`（カバレッジ・モック付き）、Node.js (`npm test`) 及び Go (`go test ./...`) を順に走らせ、コード品質と機能の正確性を検証します。  
2. **ドキュメント生成** – `docgen/docgen.py` スクリプトが YAML 設定から API/Agent の仕様書を抽出し、Markdown 形式で自動作成します。これにより最新のコードと同期した docs が常時保持されます。  
3. **AGENTS.md 更新** – 生成されたドキュメント情報を元に `AGENTS.md` を再構築し、プロジェクト内の主要なエージェント一覧が更新されます。

### 主な技術スタック
- **Python (≥3.11)**  
  - `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` を使用し、テストと YAML パースを担います。  
- **Shell** – ビルド・実行スクリプトのシェル化でクロス環境対応。  
- **Node.js / Go** – それぞれ独自に提供されるユニット／インテグレーションテストを走らせます。

### 開発フロー
```bash
# 依存パッケージの同期・ビルド
uv sync
uv build

# ドキュメント生成（Python スクリプト実行）
uv run python3 docgen/docgen.py

# テスト実行
uv run pytest tests/ -v --tb=short   # Python
npm test                               # Node.js
go test ./...                          # Go
```

### コーディング規約  
- **リンター**: `ruff` を採用し、PEP8 への準拠と静的型チェックを自動化。  

このパイプラインにより、コミット時点でテストが通過したコードのみがドキュメントへ反映されるため、常に正確かつ最新の情報を保持できます。また、複数言語環境下でも一貫したビルド・検証プロセスが実現されています。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 07:18:52*