# AGENTS ドキュメント

自動生成日時: 2025-11-27 23:34:28

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


本プロジェクトは、AI エージェントの開発・保守を円滑にするための自動化パイプラインです。  
- **主な機能**：コミットごとにテスト実行 → ドキュメント生成（`docgen.py`）→ `AGENTS.md` の差分更新という一連作業をシームレスに実施します。  
- **言語・ツール**：Python 3 と Bash をベースに構築され、依存関係は `pyyaml`, `pytest`, `pytest‑cov`, `pytest‑mock` に限定しています。また、リントには Ruff が採用されています。  
- **ビルドフロー**  
  ```bash
  uv sync          # 依存パッケージを同期
  uv build         # ビルドアーティファクト作成（必要に応じて）
  uv run python3 docgen/docgen.py   # ドキュメント生成スクリプト実行
  ```
- **テストフロー**  
  ```bash
  uv run pytest tests/ -v --tb=short    # Python テスト (pytest)
  npm test                               # JavaScript / TypeScript コンポーネントのテスト（必要に応じて）
  go test ./...                          # Go コンポーネントのテスト（必要に応じて）
  ```
- **運用上のメリット**  
  - コードベースとドキュメントが常に同期し、最新状態を保つため QA 時の不整合リスクを低減。  
  - `AGENTS.md` の手動編集不要で、CI/CD パイプラインから自動生成されることでエージェント追加・変更時の作業負担が軽減。  
- **拡張性**：新しい AI エージェントを追加する際は、該当ディレクトリに YAML 定義ファイルと必要なスクリプト／テストを書くだけで、自動生成対象となります。

このパイプラインを活用すれば、エンジニアリングチームはコード品質の維持・向上に集中できる環境が整います。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 23:34:28*