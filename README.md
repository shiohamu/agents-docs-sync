# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、プロジェクトのコミットごとに自動でテスト実行・ドキュメント生成・`AGENTS.md` の更新を行う CI パイプラインです。  
主な目的は、最新のコードベースと同期した API ドキュメントおよびエージェント一覧を常時保守し、開発者が正確で即時に参照できる情報源を提供することです。

### 主要構成

| コンポーネント | 内容 |
|-----------------|------|
| **Python スクリプト** (`docgen/docgen.py`) | YAML 定義とソースコメントから Markdown ドキュメントを生成し、`AGENTS.md` を更新します。 |
| **シェルスクリプト/Makefile** | ビルド・テストコマンドの実行や環境設定を簡易化します。 |
| **CI ワークフロー** | GitHub Actions などで `uv sync`, `uv build` を走らせ、変更が検知されるたびに自動処理をトリガーします。 |

### 依存関係

- Python  
  - `pyyaml>=6.0.3`
  - `pytest>=7.4.0`
  - `pytest-cov>=4.1.0`
  - `pytest-mock>=3.11.1`

> **備考**: Node.js (`npm test`) と Go(`go test ./...`) のテストも併せて実行します。  
> **開発環境管理ツール**: `uv` を使用して Python パッケージの同期・ビルドを行います。

### ビルド手順

```bash
# 依存関係インストールとパッケージング
uv sync          # requirements.txt 等からインストール
uv build         # バイナリや wheel の作成（必要に応じて）
```

その後、ドキュメント生成スクリプトを実行します。

```bash
uv run python3 docgen/docgen.py
```

### テスト手順

```bash
# Python 用テスト
uv run pytest tests/ -v --tb=short

# Node.js 用テスト（存在する場合）
npm test

# Go 用テスト（存在する場合）
go test ./...
```

全てのテストがパスした後に `AGENTS.md` が更新され、コミット時点で最新情報を保持します。

### コーディング規約・Lint

- **リンター**: [ruff](https://github.com/astral-sh/ruff) を使用。  
  ```bash
  ruff check .
  ```

> `uv` は Python の依存関係とビルドを高速化するため、CI 環境でのセットアップ時間短縮に寄与します。

### 使い方まとめ

1. **ローカル環境**  
   ```bash
   uv sync          # 必要なパッケージ取得
   uv run pytest    # テスト実行（Python）
   npm test         # Node.js のテスト (必要なら)
   go test ./...    # Go のテスト (必要なら)
   uv run python3 docgen/docgen.py  # ドキュメント生成と AGENTS.md 更新
   ```

2. **CI**  
   GitHub Actions 等で `uv sync`, `uv build` → テスト実行 → スクリプト実行を順に設定します。  

このワークフローにより、開発者はコミットごとに常に最新のドキュメント・エージェント一覧が反映された状態を保つことができるため、レビューや利用時の混乱を最小限に抑えることができます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 09:52:13*