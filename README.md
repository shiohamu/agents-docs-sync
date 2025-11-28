# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、コミットごとに自動でテスト実行・ドキュメント生成・AGENTS.md の更新を行う CI/CD パイプラインです。  
主な構成要素は以下の通りです。

- **使用言語**: Python (3.11+) とシェルスクリプト
- **依存関係**（Python）:
  - `pyyaml>=6.0.3`
  - `pytest>=7.4.0`
  - `pytest-cov>=4.1.0`
  - `pytest-mock>=3.11.1`

### ビルドフロー
```bash
uv sync          # プロジェクトの依存関係を同期
uv build         # パッケージビルド（必要に応じて）
uv run python3 docgen/docgen.py   # ドキュメント生成スクリプト実行
```

### テストフロー
```bash
uv run pytest tests/ -v --tb=short    # Python の単体テストとカバレッジ確認
npm test                               # JavaScript / TypeScript 用のテスト（必要に応じて）
go test ./...                          # Go モジュール用のユニットテスト
```

### コーディング規約
- **リンター**: `ruff` を使用してコード品質を保守

このプロジェクトは、変更があるたびに自動的にビルド・テスト・文書化を行い、AGENTS.md に最新情報を反映させることでチーム全体の開発フローをスムーズかつ一貫性の高いものにします。





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

*このREADME.mdは自動生成されています。最終更新: 2025-11-28 16:19:03*