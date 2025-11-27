# AGENTS ドキュメント

自動生成日時: 2025-11-27 13:21:46

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、ソースコードにコミットがあった際に自動で以下の処理を実行する CI/CD パイプラインです。  
1️⃣ **テスト実行** – Python の `pytest`（カバレッジ付き）と Node.js／Go 向けの標準的なユニットテストコマンドを並列に走らせ、全言語でコード品質が保たれているか確認します。  
2️⃣ **ドキュメント生成** – `docgen/docgen.py` を実行し、Python ソースから Sphinx 互換の Markdown ドキュメントと API リファレンスを作成します。このプロセスは `uv run python3 docgen/docgen.py` により高速化されます。  
3️⃣ **AGENTS.md の自動更新** – 上記で生成されたドキュメントやテストレポート（カバレッジ率、エラー情報など）を解析し、最新の状態に合わせて `AGENTS.md` を書き換えます。これにより、プロジェクト内の AI エージェントは常に正確な API 情報とビルドステータスを参照できます。

### 実行環境
- **Python**: 依存パッケージ `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` を使用。  
- **ビルド/実行ツール**: `uv sync`, `uv build`, `uv run`.  
- **テストスイート**: Python (`uv run pytest tests/... -v --tb=short`), Node.js (`npm test`), Go (`go test ./...`).  

### コーディング規約
プロジェクト全体は `ruff` をリンターとして採用しており、静的解析とフォーマッティングを一貫した状態で保ちます。  
このパイプラインにより、コミットごとの品質保証が自動化され、AI エージェントは最新のドキュメントやテスト結果を即座に利用できるようになります。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 13:21:46*