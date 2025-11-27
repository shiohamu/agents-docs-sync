# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、リポジトリへのコミットが発生するたびに自動的にテストを実行し、最新のドキュメントを生成して `AGENTS.md` を更新します。  
このプロジェクトは主に Python とシェルスクリプトで構成されており、CI/CD パイプライン内で以下のフローが走ります。

1. **依存関係同期** – `uv sync` でローカル環境をセットアップ  
2. **ビルド** – `uv build` によりパッケージ化（wheel 等）  
3. **文書生成** – `uv run python3 docgen/docgen.py` がプロジェクトの API/CLI ドキュメントを自動で作成し、既存の `AGENTS.md` を差分更新  

テストは多言語対応です。Python の単体・統合テスト (`pytest`) に加え、Node.js と Go でもそれぞれのユニットテストが実行されます。

| コマンド | 概要 |
|---|---|
| `uv sync` | uv を使った依存関係インストール（pyyaml, pytest 系など） |
| `uv build` | ビルドアーティファクトを生成 |
| `uv run python3 docgen/docgen.py` | ドキュメント生成スクリプト実行 |
| `uv run pytest tests/ -v --tb=short` | Python テストの高速走査 |
| `npm test` | Node.js プロジェクトテスト（必要に応じて） |
| `go test ./...` | Go モジュール全体を対象としたテスト |

### 主要依存パッケージ

- **pyyaml** ≥6.0.3 – YAML ファイルの読み書き  
- **pytest** ≥7.4.0, **pytest-cov** ≥4.1.0, **pytest-mock** ≥3.11.1 – テストフレームワークとカバレッジ、モックサポート  

### コーディング規約

- リンター: `ruff` を使用し、一貫したコード品質を保ちます。  
  - フォーマットや静的解析は CI の段階で自動チェックされるよう設定済みです。

---

#### 使用例（ローカル開発時）

```bash
# 環境構築・ビルド
uv sync && uv build

# ドキュメント生成と AGENTS.md 更新
uv run python3 docgen/docgen.py

# テスト実行
uv run pytest tests/ -v --tb=short
npm test          # Node.js が必要な場合
go test ./...     # Go モジュールがある場合
```

このワークフローを CI の `push` や `pull request` 時に組み込むことで、常に最新のドキュメントと正確なテスト結果を保つことができます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 21:57:27*