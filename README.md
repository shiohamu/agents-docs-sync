# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、Python とシェルスクリプトで構築された CI/CD パイプラインです。このプロジェクトは以下の機能を自動化します。  

* **テスト実行** – コミット時に `pytest`（Python）、`npm test`（Node.js）および `go test ./...` を走らせ、コード品質と互換性を保証します。  
* **ドキュメント生成** – Python スクリプト (`docgen/docgen.py`) が実行され、ソースから API 仕様や使用例などの最新ドキュメントが作成されます。  
* **AGENTS.md の更新** – 自動で生成された情報を `AGENTS.md` に書き込み、プロジェクト全体におけるエージェント一覧と詳細を常に同期させます。

## 技術スタック

| 主要言語 | 使用ツール |
|----------|------------|
| Python   | uv (パッケージ管理・ビルド)、ruff（リンター） |
| Shell    | - |

### 主な依存関係
```bash
pyyaml>=6.0.3
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
```

## ビルド手順

```sh
# ① 必要パッケージの同期
uv sync

# ② パッケージをビルド（wheel 等）
uv build

# ③ ドキュメント生成スクリプト実行
uv run python3 docgen/docgen.py
```

## テスト手順

```sh
# Python ユニットテスト (詳細出力、短いバックトレース)
uv run pytest tests/ -v --tb=short

# Node.js のユニット／統合テスト
npm test

# Go プロジェクトの全パッケージに対するテスト実行
go test ./...
```

## コーディング規約と品質保証

* **リンター**: `ruff` を使用して PEP8 に準拠したコードスタイルを維持します。  
* テストカバレッジは `pytest-cov` で測定し、最低限の基準値に達することが期待されます。

## 目的

このリポジトリは「コミット → ビルド・テスト → ドキュメント生成」サイクルを一貫したワークフローとして提供します。  
- **開発者** はコードを書くだけで、ビルドと文書化が自動的に行われるため手間が減ります。  
- **運用担当者** や **利用者** は常に最新のエージェント情報を `AGENTS.md` から確認でき、導入や拡張時の障壁が低くなります。

---





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

*このREADME.mdは自動生成されています。最終更新: 2025-11-28 10:12:31*