# AGENTS ドキュメント

自動生成日時: 2025-11-26 14:14:09

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、コミットごとに自動でテストを実行し、最新のドキュメントを生成して `AGENTS.md` を更新する CI/CD パイプラインです。  
主なフローは以下の通りです。

1. **依存関係インストール** – Python のパッケージ (`pyyaml`, `pytest`, `pytest‑cov`, `pytest-mock`) と、必要に応じて npm や Go モジュールをインストールします。  
   ```bash
   uv sync          # pyproject.toml から依存関係を同期
   ```

2. **ビルド** – プロジェクトのパッケージングやバイナリ生成が必要な場合に実行されます。
   ```bash
   uv build         # ビルドアーティファクト作成（例: wheel）
   ```

3. **テスト実行**  
   - Python：`pytest tests/ -v --tb=short`
   - JavaScript / Node.js：`npm test`
   - Go：`go test ./...`  
   すべてのテストが成功しなければビルドは失敗します。

4. **ドキュメント生成** – `docgen/docgen.py` がコードベースと YAML 設定から最新の API/機能説明を抽出し、Markdown ドキュメントに変換します。  
   ```bash
   uv run python3 docgen/docgen.py
   ```

5. **AGENTS.md 更新** – 生成されたドキュメント内のエージェント情報（名前・概要・入力/出力フォーマットなど）をパースし、`AGENTS.md` を差分反映します。これにより、コード変更と同時に文書が常に最新状態になります。

6. **静的解析** – コーディング規約は `ruff` によってチェックされます。CI での lint 結果を必ず確認してください。
   ```bash
   ruff check .
   ```

### 開発者向けローカル実行手順

```bash
# 必要なツールがインストール済みか確認（uv, python3.11+）
uv sync          # 依存関係を取得
uv run pytest tests/ -v --tb=short   # Python テスト
npm test         # Node.js のテスト (必要に応じて)
go test ./...    # Go モジュールのテスト

# ドキュメントと AGENTS.md を手動で更新したい場合は
uv run python3 docgen/docgen.py      # Markdown 生成
```

### パイプライントリガー

- GitHub Actions / CI サーバ上では `push` または `pull_request` イベント時に自動実行されます。  
- 成功したビルドとテストの後、コミットがマージされた際に生成されたファイルを含むプッシュが行われるよう設定されています。

### 重要ポイント

| 項目 | 内容 |
|------|------|
| **目的** | コード変更時に自動で最適化・ドキュメントの整合性確保 |
| **主言語** | Python（docgen、テスト） + Shell スクリプト |
| **依存関係管理** | `uv` を利用した PDM 形式 (pyproject.toml) |
| **ビルド・実行コマンド** | uv sync → uv build → uv run python3 docgen/docgen.py |
| **テスト環境** | pytest, npm test, go test の三言語統合 |
| **Linting** | ruff |

この構成により、エージェントの機能追加や変更が行われるたびに `AGENTS.md` を手動で更新する必要はなくなり、常に最新かつ正確な情報を開発者・利用者へ提供できます。
**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->

<!-- MANUAL_END:setup -->
### 前提条件





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


---


## ビルドおよびテスト手順

### ビルド手順


```bash
uv sync
uv build
uv run python3 docgen/docgen.py
```


### テスト実行


```bash
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```


---

## コーディング規約

<!-- MANUAL_START:other -->

<!-- MANUAL_END:other -->



### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```





---

## プルリクエストの手順

<!-- MANUAL_START:pr -->

<!-- MANUAL_END:pr -->
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



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 14:14:09*