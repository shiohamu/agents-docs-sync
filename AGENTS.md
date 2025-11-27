# AGENTS ドキュメント

自動生成日時: 2025-11-27 09:55:30

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


本プロジェクトは、AI エージェントのドキュメントを常に最新状態に保つことを目的とした CI/CD パイプラインです。  
コミットが行われるたびに自動で以下の処理が実施されます。

1. **環境構築** – `uv sync` で Python の依存関係（pyyaml, pytest 系など）をインストールし、必要ならシェルスクリプトやその他言語用ツールもセットアップします。  
2. **ビルドと検証** – `uv build` によってプロジェクトのビルドアーティファクトが生成され、その後に `uv run python3 docgen/docgen.py` を実行して最新のドキュメントを作成します。  
   - ドキュメントは YAML で記述されたエージェント定義から自動抽出し、Markdown フォーマットへ変換されます。  
3. **テスト** – `uv run pytest tests/`（Python）、`npm test`（Node.js）および `go test ./...`（Go）の各言語に対して単体・統合テストを実行し、品質保証を行います。  
4. **AGENTS.md の更新** – 生成されたドキュメント内容が AGENTS.md に反映されるようスクリプトで差分を書き込みます。これにより手動編集の必要はなくなります。

### 主な技術スタック
- **Python / Shell**  
  - `pyyaml>=6.0.3`：YAML パーサー（エージェント定義読み取り用）  
  - `pytest`, `pytest-cov`, `pytest-mock`：テスト実行・カバレッジ測定・モック作成
- **CI ツール** – GitHub Actions 等で自動化。  
- **Linting / コーディング規約** – `ruff` を使用し、一貫したコード品質を保ちます。

### 期待される効果
- ドキュメントの手作業更新が不要になり、エージェント仕様変更時に即座に反映。  
- CI パイプラインでテスト失敗やビルド不具合を早期検知し、品質低下リスクを最小化。  
- 複数言語（Python, Node.js, Go）プロジェクトでも一元管理が可能。

このパイプラインにより、AI エージェント開発チームはコードとドキュメントの整合性を保ちながら高速なリリースサイクルを実現できます。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 09:55:30*