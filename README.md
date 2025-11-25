# agents-docs-sync

`agents‑docs‑sync`は、リポジトリにコミットがあるたびに自動で以下を実行するCI/CDパイプラインです。

- **テストの実行**  
  - Python: `uv run pytest tests/ -v --tb=short`
  - Node.js: `npm test`（必要な場合）
  - Go: `go test ./...`

- **ドキュメント生成**  
  - `python3 docgen/docgen.py` を実行し、テスト結果やコードコメントから最新のAPI・使用方法を含む Markdown ドキュメントを作成します。

- **AGENTS.md の自動更新**  
  - スクリプトがプロジェクト内にあるエージェント定義ファイル（YAML 等）を解析し、`AGENTS.md` を最新状態へ書き換えます。これによりドキュメントと実装の整合性が保たれます。

## 技術スタック

| カテゴリ | 言語 / ツール |
|----------|----------------|
| スクリプト言語 | Python 3.x, Shell (bash) |
| パッケージマネージャ | uv（Python） |

## 主な依存関係

- **PyYAML** ≥ 6.0.3  
- **pytest** ≥ 7.4.0  
- **pytest‑cov** ≥ 4.1.0  
- **pytest‑mock** ≥ 3.11.1  

（`uv sync` でこれらをインストール）

## ビルド手順

```bash
# 必要なパッケージの同期とビルド
$ uv sync          # deps install / lockfile update
$ uv build         # optional packaging step (e.g., wheel)
$ uv run python3 docgen/docgen.py  # ドキュメント生成
```

## テスト実行

```bash
# Python のテスト
$ uv run pytest tests/ -v --tb=short

# Node.js（必要に応じて）
$ npm test

# Go (モノレポ構成の場合)
$ go test ./...
```

## コーディング規約とスタイルチェック

- **リンター**: `ruff` を使用し、Python のコード品質を保ちます。  
  ```bash
  $ ruff check .
  ```

---

このプロジェクトは、コミットごとの自動化によりドキュメントの鮮度とエージェント仕様書（AGENTS.md）の正確性を保証し、開発者が常に最新情報へアクセスできるよう設計されています。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 06:33:33*