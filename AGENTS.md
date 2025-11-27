# AGENTS ドキュメント

自動生成日時: 2025-11-27 13:57:45

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


`agents-docs-sync` は、Python とシェルスクリプトで構築された自動化パイプラインです。  
コミットごとに次の処理を実行し、AGENTS.md を最新状態へ保ちます。

- **テスト** – `uv run pytest tests/ -v --tb=short`（Python）、`npm test`（JavaScript）および `go test ./...` でコードベース全体の動作検証とカバレッジ測定を行います。  
- **ドキュメント生成** – `uv run python3 docgen/docgen.py` が YAML 設定 (`pyyaml>=6.0.3`) を読み込み、Python コードやコメントから Markdown ドキュメントを自動作成します。  
- **AGENTS.md 更新** – 生成されたドキュメントとエージェントのメタ情報を組み合わせて AGENTS.md に反映させます。

ビルド手順は次通りです:

1. `uv sync` ― 必要な Python ライブラリ（pytest, pytest‑cov, pytest‑mock など）をインストール  
2. `uv build` ― ビルド用の環境設定  
3. 上記テスト・生成ステップ

コーディング規約は **ruff** を使用してコード品質と一貫性を確保します。  

このパイプラインにより、コミット前に常に最新かつ正確なエージェントドキュメントが提供されるため、開発者間の情報共有やレビュー作業がスムーズになります。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 13:57:45*