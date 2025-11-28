# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
本リポジトリは、コミットごとに自動的にテストを実行し、最新のドキュメントを生成・更新するCI/CDパイプラインです。  
主な機能は次の通りです。

- **Python テスト**：`pytest`, `pytest-cov`, `pytest-mock` を使用してユニット／統合テストを実行し、カバレッジ情報も収集します。
- **ドキュメント生成**：プロジェクト内の構成ファイルやコードコメントから Markdown ドキュメント（例: AGENTS.md）を自動作成・更新します。スクリプトは `docgen/docgen.py` で実装されています。
- **マルチ言語サポート**：Python のテストに加えて、Node.js (`npm test`) と Go (`go test ./...`) 用のテストも同時に走らせることができます。

### 環境構築
```bash
# 依存関係をインストールし環境を同期する
uv sync

# ビルド（バイナリ・wheel 等）
uv build

# ドキュメント生成スクリプト実行
uv run python3 docgen/docgen.py
```

### テスト実行
```bash
# Python のテストとカバレッジ報告を取得
uv run pytest tests/ -v --tb=short

# Node.js プロジェクトのユニットテスト
npm test

# Go モジュール全体のテスト
go test ./...
```

### コーディング規約・Lint
- **リンター**：`ruff`
  ```bash
  ruff check .
  ```

これらを組み合わせることで、コード変更ごとに自動的に品質チェックが行われ、ドキュメントは常に最新の状態になります。





## 使用技術

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-28 16:40:44*