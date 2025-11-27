# AGENTS ドキュメント

自動生成日時: 2025-11-27 13:41:14

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


**目的**  
`agents-docs-sync` は、コミットが行われるたびにテスト実行・ドキュメント生成を自動化し、その結果で `AGENTS.md` を更新する CI/CD パイプラインです。AI エージェントや開発者は、このプロジェクトによって最新の API ドキュメントとエージェント一覧が常に同期されるため、手作業でのメンテナンスを削減できます。

**主な機能**

- **CI トリガー**  
  - GitHub Actions／GitLab CI などから `push` イベントで起動。  
  - パイプラインは以下のステップに分かれます。
    1. 必要パッケージインストール (`uv sync`)  
    2. ビルド（ビルダー・バンドラー等）(`uv build`)  
    3. ドキュメント生成スクリプト実行 (`uv run python3 docgen/docgen.py`)

- **テスト統合**  
  - Python: `pytest`, `pytest-cov`, `pytest-mock` を使用し、詳細なカバレッジとモック機能を提供。  
  - Node.js：`npm test`（Jest 等）でフロントエンド・ユーティリティのテスト実行。  
  - Go: `go test ./...` によりバックエンド／CLI コード全体を検証。

- **ドキュメント生成**  
  - YAML 定義 (`pyyaml>=6.0.3`) を読み込み、Python スクリプトで Markdown ドキュメントに変換。  
  - `AGENTS.md` は自動的に更新され、新しいエージェント情報やパラメータが反映。

- **コード品質**  
  - 静的解析・リンティングは `ruff` を採用し、PEP8 等のスタイルガイドを強制。  

**開発者向け手順**

1. リポジトリクローン後に依存関係を解決  
   ```bash
   uv sync
   ```
2. ビルド（必要なら）  
   ```bash
   uv build
   ```
3. ドキュメント生成と AGENTS.md 更新のローカル実行  
   ```bash
   uv run python3 docgen/docgen.py
   ```
4. テストをすべて走らせるには  
   ```bash
   uv run pytest tests/ -v --tb=short
   npm test
   go test ./...
   ```

**エージェント情報の構造**

- `AGENTS.md` はセクションごとに分割され、各エージェントは以下を含む  
  * 名前・説明  
  * 使用言語／環境（Python, Shell 等）  
  * コマンド例やインタフェース仕様  
  * テストケースの概要  

これらが統合された形で `AGENTS.md` に記載されるため、ドキュメントと実装コードを常に同期させた状態で参照できます。
**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->

<!-- MANUAL_END:setup -->
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 13:41:14*