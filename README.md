# agents-docs-sync

agents-docs-sync は、コミットごとに自動でテスト実行・ドキュメント生成を行い、その結果を AGENTS.md に反映させる CI/CD パイプラインです。  
Python とシェルスクリプトの組み合わせで構成されており、以下のようなワークフローが想定されています。

* **テスト実行** – `pytest`（Python）、`npm test`（Node.js）と `go test ./...` を順に走らせることで、多言語プロジェクト全体を網羅的に検証します。  
* **ドキュメント生成** – `docgen/docgen.py` が YAML 形式の設定ファイルから API ドキュメントや利用例を書き出し、AGENTS.md を自動更新します。  
* **ビルド・デプロイ** – uv（Python パッケージマネージャ）を使い依存関係同期 (`uv sync`) とパッケージ化(`uv build`)、スクリプト実行 (`uv run python3 docgen/docgen.py`) を一連のビルドステップとしてまとめています。  

### 主要な技術スタック

| コンポーネント | バージョン要件 |
|-----------------|---------------|
| Python          | `pyyaml>=6.0.3`<br>`pytest>=7.4.0`<br>`pytest-cov>=4.1.0`<br>`pytest-mock>=3.11.1` |
| シェルスクリプト | 標準的な POSIX 互換シェル（Bash 等） |

### コーディング規約

* **リンタ**：Ruff を使用して静的解析とコードフォーマットを統一します。  
* テストは `-v` オプションで詳細出力、短いトレースバック (`--tb=short`) で可読性向上。

### ビルド・テストコマンド

```bash
# Build（依存関係同期＋パッケージ化）
uv sync
uv build

# ドキュメント生成と AGENTS.md の更新
uv run python3 docgen/docgen.py

# テスト実行
uv run pytest tests/ -v --tb=short   # Pythonテスト
npm test                               # Node.jsテスト
go test ./...                          # Go言語のユニットテスト
```

### 期待される成果物

* **AGENTS.md**：最新の API スペックと使用例を含むマークダウンファイル。  
* **ドキュメントディレクトリ**（`docs/` 等）：自動生成された HTML や Markdown ファイル。  
* テストカバレッジレポートやログは CI 環境に出力され、変更履歴と共にプルリクエストで確認可能。

このプロジェクトを導入することで、開発者はコードの品質チェックだけでなく、ドキュメントの最新化まで一括して管理できるため、継続的デリバリー（CD）環境下でも整合性と可読性が保たれます。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 06:24:58*