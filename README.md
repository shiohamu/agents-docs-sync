# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、リポジトリにコミットがあるたびに自動でテストを実行し、ドキュメント（`docs/` ディレクトリ）と `AGENTS.md` を再生成するパイプラインです。  
主な特徴は次の通りです。

- **言語**: Python とシェルスクリプトで構成されており、Python 3.11+ が必要
- **依存関係**
  - `pyyaml>=6.0.3` – YAML の読み書きに使用  
  - `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` – テスト実行とカバレッジ収集
- **ビルド手順**
  ```bash
  uv sync          # 依存関係をインストール/同期
  uv build         # パッケージのビルド（必要に応じて）
  uv run python3 docgen/docgen.py   # ドキュメント生成スクリプト実行
  ```
- **テストコマンド**  
  - Python: `uv run pytest tests/ -v --tb=short`  
  - Node.js (npm): `npm test`（必要に応じて）  
  - Go: `go test ./...`
- **コード品質**  
  - Linting は `ruff` を使用。プロジェクトルートで `uv run ruff check .` によりスタイルチェックが可能

このリポジトリは、コミット時に自動化された CI/CD ワークフロー（GitHub Actions 等）を想定して設計されており、コードの変更と同時に最新のドキュメント・エージェント一覧 (`AGENTS.md`) を常に同期させることで、開発者が手作業で更新する負担を大幅に軽減します。

## 使用技術

- Python
- Shell

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 14:11:48*