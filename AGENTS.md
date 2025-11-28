# AGENTS ドキュメント

自動生成日時: 2025-11-28 16:41:12

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


`agents‑docs‑sync` は、プロジェクトにコミットが入るたびに以下の処理を自動で実行するパイプラインです。  
- **テスト**（Python・Node.js・Go）を並列に走らせてコード品質を保証します。  
- コードベースから最新ドキュメント（YAML/Markdown など）を生成し、`AGENTS.md` を自動的に更新します。  

この仕組みにより、手作業での文書管理が不要になり、常にリポジトリ内に正確なエージェント仕様が保持されます。

## 実行フロー

1. **コミット検知**  
   GitHub Actions 等を利用して `push` イベントを監視。  

2. **ビルド環境のセットアップ** (`uv sync`)  
   - 依存パッケージ（pyyaml, pytest 系）と Python 環境が自動でインストールされます。  
   - `uv build` によりプロジェクトをビルドし、配布可能なアーティファクトへ変換します。

3. **文書生成** (`uv run python3 docgen/docgen.py`)  
   - ソースコードとメタデータから Markdown／YAML を作成。  
   - 生成された内容は `AGENTS.md` に差分として反映されます。

4. **テスト実行**  
   ```bash
   uv run pytest tests/ -v --tb=short      # Python テスト
   npm test                                 # Node.js テスト（必要に応じて）
   go test ./...                            # Go テスト（モノレポ内のパッケージ全体）
   ```
   失敗した場合はビルドを中断し、コミットが拒否されます。

5. **CI/CD の完了**  
   - 成功時に `AGENTS.md` が更新された状態でプッシュ。  
   - 必要なら PR コメントや Slack 通知等のアクションも併せて実行可能です。

## 主要ファイル

- `docgen/docgen.py`: ドキュメント生成ロジック（Python スクリプト）。  
- `.github/workflows/ci.yml` (想定): 上記ステップを GitHub Actions に設定。  
- `tests/*`: 各言語のテストケース。  

## 開発者向け手順

1. **uv のインストール**（公式サイトまたは `pipx install uv`）。  
2. ビルド環境構築: ```bash
   uv sync && uv build
   ```
3. ドキュメント生成をローカルで確認:
   ```bash
   uv run python3 docgen/docgen.py
   ```
4. テスト実行（すべての言語）:
   ```bash
   uv run pytest tests/ -v --tb=short && npm test && go test ./...
   ```

## 重要ポイント

- **自動化**: コミット時にテスト・ドキュメント生成が連携して走るため、手作業での更新漏れを防止。  
- **多言語対応**: Python のみならず Node.js と Go のテストも同一パイプライン内で実行。  
- **コード品質**: `ruff` をリントツールとして使用し、一貫したスタイルチェックが組み込まれています。

これにより、エージェントのドキュメントと実装を常に同期させつつ、高い信頼性で CI/CD パイプラインを運用できます。
**使用技術**: python


## プロジェクト構造
```
agents-docs-sync/
 ├─ docgen/
 │  ├─ collectors/
 │  │  ├─ collector_utils.py
 │  │  └─ project_info_collector.py
 │  ├─ detectors/
 │  │  ├─ configs/
 │  │  │  ├─ go.toml
 │  │  │  ├─ javascript.toml
 │  │  │  ├─ python.toml
 │  │  │  └─ typescript.toml
 │  │  ├─ base_detector.py
 │  │  ├─ config_loader.py
 │  │  ├─ detector_patterns.py
 │  │  ├─ plugin_registry.py
 │  │  └─ unified_detector.py
 │  ├─ generators/
 │  │  ├─ parsers/
 │  │  │  ├─ base_parser.py
 │  │  │  ├─ generic_parser.py
 │  │  │  ├─ js_parser.py
 │  │  │  └─ python_parser.py
 │  │  ├─ agents_generator.py
 │  │  ├─ api_generator.py
 │  │  ├─ base_generator.py
 │  │  └─ readme_generator.py
 │  ├─ hooks/
 │  │  ├─ tasks/
 │  │  │  └─ base.py
 │  │  ├─ config.py
 │  │  └─ orchestrator.py
 │  ├─ index/
 │  │  └─ meta.json
 │  ├─ models/
 │  │  ├─ agents.py
 │  │  └─ config.py
 │  ├─ prompts/
 │  │  ├─ agents_prompts.yaml
 │  │  ├─ commit_message_prompts.yaml
 │  │  └─ readme_prompts.yaml
 │  ├─ rag/
 │  │  ├─ chunker.py
 │  │  ├─ embedder.py
 │  │  ├─ indexer.py
 │  │  ├─ retriever.py
 │  │  └─ validator.py
 │  ├─ utils/
 │  │  ├─ cache.py
 │  │  ├─ exceptions.py
 │  │  ├─ file_utils.py
 │  │  ├─ llm_client.py
 │  │  ├─ markdown_utils.py
 │  │  └─ prompt_loader.py
 │  ├─ config.yaml
 │  ├─ config_manager.py
 │  ├─ docgen.py
 │  └─ hooks.yaml
 ├─ docs/
 ├─ scripts/
 ├─ tests/
 ├─ AGENTS.md
 ├─ PROJECT_MANAGEMENT_GUIDE.md
 ├─ README.md
 ├─ RELEASE.md
 ├─ install.sh
 ├─ pyproject.toml
 ├─ requirements-docgen.txt
 ├─ requirements-test.txt
 └─ setup.sh
```






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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-28 16:41:12*