# AGENTS ドキュメント

自動生成日時: 2025-11-25 18:17:49

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

**agents-docs-sync** は、コミットが行われるたびに自動でテストを実行し、ドキュメント（YAML を基にした Markdown 形式）を生成して `AGENTS.md` ファイルを更新するパイプラインです。CI/CD 環境では GitHub Actions 等のワークフローからこのリポジトリがチェックアウトされ、以下の手順で実行されます。

1. **依存関係インストール**  
   ```bash
   uv sync          # pyproject.toml への記述に基づき Python のパッケージを解決・インストール
   ```
2. **ビルド & ドキュメント生成**  
   - `uv build` はプロジェクトのビルドアーティファクト（例: wheel）を作成します。  
   - `uv run python3 docgen/docgen.py` が実行され、YAML で定義されたエージェント情報から Markdown ドキュメントを生成し、既存の `AGENTS.md` を差分反映させます。
3. **テスト実行**  
   - Python テスト: `uv run pytest tests/ -v --tb=short`（pytest, pytest-cov, pytest-mock が利用）  
   - Node.js 版のテストがある場合は `npm test`、Go モジュールの場合は `go test ./...` を実行します。  

> **コーディング規約**: 全ての Python コードに対して Ruff ライナーを適用し、一貫したコード品質とスタイルチェックを保証しています。

### 主要依存関係
- `pyyaml>=6.0.3` – YAML パーサ  
- `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` – テストフレームワークと補助ツール  

### 使い方
```bash
# 開発環境のセットアップ（uv がインストール済みであることが前提）
uv sync

# ドキュメント生成・AGENTS.md の更新を手動実行したい場合
uv run python3 docgen/docgen.py

# テストのみ実行したいときは
uv run pytest tests/ -v --tb=short
```

このプロジェクトにより、ドキュメントの整合性がコード変更ごとに保証されるため、エージェント仕様書やチーム内共有資料を常に最新状態で保つことができます。

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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 18:17:49*