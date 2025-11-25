# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
agents‑docs‑sync は、コミットごとに自動的にテストを実行し、最新のドキュメントを生成して `AGENTS.md` を更新するパイプラインです。  
主な機能は以下の通りです。

- **CI/CD ワークフロー**: コードが push されると GitHub Actions が起動し、テスト実行 → ドキュメント生成 (`docgen/docgen.py`) → `AGENTS.md` の差分反映という一連の処理を順次走らせます。  
- **多言語サポート**: Python（ドキュメンテーションジェネレータ）、Shell スクリプトで構成されており、Python だけではなく `npm test` や Go のユニットテストも同時に走らせます。  
- **依存関係管理**: `uv` を使用して Python パッケージ（pyyaml, pytest 系）とビルドツールを解決します。Go と Node.js はそれぞれの標準的なコマンドでテストが実行されます。  

### 主要ファイル

- **docgen/docgen.py**: ドキュメント生成ロジック（YAML を読み込み、Markdown のテンプレートへ変換）。  
- **AGENTS.md**: 自動更新対象のドキュメントハブ。  
- **.github/workflows/***：CI/CD 定義ファイル。

### 依存関係

| 言語 | パッケージ |
|------|------------|
| Python | `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` |
| Node.js | 省略（テストフレームワークは npm test にて管理） |
| Go | 標準ライブラリ＋go.modで定義 |

### ビルド & テスト

```bash
# 環境セットアップ (Python)
uv sync            # 仮想環境作成と依存パッケージインストール
uv build           # パッケージビルド（必要に応じて）

# ドキュメント生成
uv run python3 docgen/docgen.py

# テスト実行 (Python)
uv run pytest tests/ -v --tb=short

# Node.js のテスト
npm test

# Go のテスト
go test ./...
```

### コーディング規約

- Python ソースは `ruff` で linting を強制します。  
- スタイルガイドに従い、PEP8 準拠を目指してください。

このリポジトリを利用することで、コードベースとドキュメントが常に同期し、手動更新の手間を大幅に削減できます。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 18:17:17*