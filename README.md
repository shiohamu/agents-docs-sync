# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、リポジトリにコミットがあるたびに自動的にテストを実行し、ドキュメント（`AGENTS.md` を含む）を生成・更新する CI/CD パイプラインです。  
主な機能は以下の通りです。

- **CI ワークフロー**：コミット時に `uv sync`, `uv build`, そして Python スクリプトでドキュメント生成 (`docgen/docgen.py`) を順次実行します。
- **テスト自動化**：
  - Python: `pytest`、コードカバレッジは `pytest-cov`。モックライブラリとして `pytest-mock` が使用されます。
  - Node.js と Go のユニットテストも併せて実行し、多言語プロジェクト全体の品質を保証します。
- **ドキュメント管理**：生成された Markdown ファイルは自動でコミットに追加され、リポジトリ内の `AGENTS.md` が常に最新状態になります。
- **依存関係とビルドツール**：
  - Python パッケージマネージャーとして `uv` を使用。  
    ```bash
    uv sync      # 必要なパッケージをインストール
    uv build     # ビルド用設定の生成（必要に応じて）
    ```
- **テスト実行コマンド**：
  - Python：`uv run pytest tests/ -v --tb=short`
  - Node.js：`npm test`
  - Go：`go test ./...`
- **コード品質**：全ファイルは `ruff` によって静的解析・フォーマットチェックが行われます。  
  ```bash
  ruff check .
  ```

このプロジェクトを利用することで、継続的に整合性の高いドキュメントとテスト結果を保ちつつ、開発者はコード変更に集中できる環境が提供されます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 09:55:07*