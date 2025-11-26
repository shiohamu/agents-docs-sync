# AGENTS ドキュメント

自動生成日時: 2025-11-26 13:30:15

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


`AGENTS.md` はプロジェクト内のすべての AI エージェントを一元管理し、エンジニアや自動化ツールが最新状態で参照できるようにするためのドキュメントです。  
このリポジトリでは **コミットごとに**以下の処理をパイプラインで実行して `AGENTS.md` を常に同期させます。

- **テスト実行**
  - Python: `uv run pytest tests/ -v --tb=short`
  - JavaScript/NPM：`npm test`
  - Go：`go test ./...`
- **ドキュメント生成**  
  `docgen/docgen.py` が各エージェントの YAML 設定 (`agents/*.yaml`) を読み込み、Markdown と HTML の両方を出力します。  
  ビルド時は以下コマンドで依存関係とビルド環境を整えます。
  ```bash
  uv sync          # プロジェクトのPythonパッケージをインストール・同期
  uv build         # 必要に応じてバイナリやwheel を生成（CI 用）
  uv run python3 docgen/docgen.py   # ドキュメント作成スクリプト実行
  ```
- **AGENTS.md 自動更新**  
  `docgen` が生成した Markdown ファイルを結合し、既存の `AGENTS.md` を差分だけ書き換えます。これにより手動でファイルを書き直す必要がなくなります。

### エージェント定義
- 各エージェントは **YAML** 形式（例：`agents/assistant.yaml`）で以下の情報を保持します。
  - `name`: エージェント名  
  - `description`: 機能概要  
  - `commands`: 実行可能コマンドや API スキーマ
- ドキュメント生成時に YAML をパースし、コードコメントと照合して矛盾がないか検証します。  

### コーディング規約・品質保証
- **リンター**: `ruff` が Python ソースを静的解析し PEP8 への準拠を確認します。
- テストカバレッジは `pytest-cov >=4.1.0` を使用して測定。CI パイプラインで最低限のカバー率が確保されていることを保証します。

### CI/CD の流れ
```
┌─ Commit ────────► Build │  (uv sync → uv build)
│                 ▲      │
│                 │      ▼
│           Test & Lint   │  (pytest, npm test, go test, ruff)
│                 │      │
├────────────────────────┘
│
▼
Generate Docs          ← docgen/docgen.py
|
Update AGENTS.md       ← merge generated Markdown into repo root
```

この仕組みにより、エージェントに関する情報はコードベースと常に同期し、新しい機能追加や変更が即座にドキュメントへ反映されます。AI エージェントを利用・拡張する際には `AGENTS.md` を参照して最新の仕様を把握してください。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 13:30:15*