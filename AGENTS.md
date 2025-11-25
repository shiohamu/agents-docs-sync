# AGENTS ドキュメント

自動生成日時: 2025-11-26 00:16:07

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

`agents-docs-sync` は、コミットごとに自動でテスト実行・ドキュメント生成を行い、その結果を `AGENTS.md` に反映させる CI/CD パイプラインです。  
主要な技術スタックは **Python** と **Shell スクリプト** で構成され、以下のように動作します。

### 主な機能
- **テスト実行**: `uv run pytest`（Python）、`npm test`（JavaScript）および `go test ./...`（Go）の各言語向けテストを並列で走らせます。  
- **ドキュメント生成**: Python スクリプト (`docgen/docgen.py`) が API 定義やコードコメントから Markdown ドキュメントを自動作成します。  
- **AGENTS.md の更新**: 生成されたドキュメントの内容と構造に合わせて `AGENTS.md` を再生成し、最新情報を常に反映させます。

### 開発環境
| コンポーネント | バージョン要件 |
|-----------------|---------------|
| Python          | 3.10+         |
| Shell           | Bash ≥5       |

#### 主な依存パッケージ（Python）
- `pyyaml>=6.0.3`
- `pytest>=7.4.0`
- `pytest-cov>=4.1.0`
- `pytest-mock>=3.11.1`

### ビルド・テストフロー
| ステップ | コマンド |
|----------|---------|
| **ビルド** | ```bash\nuv sync && uv build && uv run python3 docgen/docgen.py\``` |
| **テスト** | ```bash\nuv run pytest tests/ -v --tb=short\nnpm test\ngo test ./...\n```

### コーディング規約
- リンター: `ruff`（Pythonコードは PEP8 と一貫性を保ちます）

---

このパイプラインにより、各コミットでテストが失敗した場合やドキュメントの不整合が検出された際には即座にフィードバックされ、チーム全体が最新かつ正確な情報へアクセスできるようになります。

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
### 前提条件

- Python 3.12以上



### 依存関係のインストール


#### Python依存関係

```bash

uv sync

```






### LLM環境のセットアップ




#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください
<!-- MANUAL_END:setup -->

---

## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順


['uv sync', 'uv build', 'uv run python3 docgen/docgen.py']


### テスト実行



#### APIを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
npm test
```

#### ローカルLLMを使用する場合

```bash
npm test
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
go test ./...
```

#### ローカルLLMを使用する場合

```bash
go test ./...
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。
<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->
### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```
<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:pr -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   
   
   uv run pytest tests/ -v --tb=short
   
   npm test
   
   go test ./...
   
   
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:pr -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 00:16:07*