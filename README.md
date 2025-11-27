# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、リポジトリへのコミットごとに自動でテストを実行し、ドキュメント生成スクリプト (`docgen/docgen.py`) を走らせて `AGENTS.md` の内容を最新の状態へ更新するパイプラインです。  
Python 3.x とシェルベースのビルド／デプロイスクリプトで構成され、CI/CD 環境（GitHub Actions 等）にそのまま組み込めます。

### 主な機能
- **テスト実行** – `pytest` を使いユニット・カバレッジチェックを自動化。  
  - Python 用: `uv run pytest tests/ -v --tb=short`
  - Node.js 用: `npm test`
  - Go 用: `go test ./...`
- **ドキュメント生成** – YAML 設定ファイルから API ドキュメントを作成し、`AGENTS.md` を更新。  
  実行コマンドは `uv run python3 docgen/docgen.py`。
- **依存関係管理** – `pyproject.toml` に記載されたパッケージ（pYYaml, pytest 系など）を `uv sync` でインストールし、ビルド時に `uv build` を使用。

### 開発環境セットアップ
```bash
# 必要なツールのインストール (例: uv)
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクト依存関係を同期
uv sync

# ビルド（ビンドリファイルやコンパイラ等が必要なら）
uv build
```

### 実行手順
1. コミット／プッシュ時に CI がトリガーされるよう設定。  
2. 上記テストコマンドを実行し、失敗した場合はビルド停止。  
3. 成功すれば `docgen/docgen.py` を走らせて最新のドキュメントと AGENTS.md を生成。  

### コーディング規約
- **リンター**: ruff（Python の静的解析ツール）を用いてコード品質を保つ。

これにより、リポジトリ内の API ドキュメンテーションは常に最新かつ正確な状態が保証されます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 13:24:10*