# AGENTS ドキュメント

自動生成日時: 2025-11-28 16:19:39

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


This project implements an automated CI/CD pipeline that keeps the repository’s documentation in sync with its codebase.  
Every time you push or commit, the following steps are executed:

1. **Run tests** – A comprehensive test suite is run using `pytest` (with coverage and mock support) for Python modules, while also invoking any JavaScript (`npm`) and Go (`go test ./...`) tests that may exist in sub‑projects.
2. **Generate documentation** – The script located at `docgen/docgen.py` collects information from the codebase, converts it into Markdown/HTML format, and outputs up-to-date docs.
3. **Update AGENTS.md automatically** – After doc generation finishes, a small helper updates the central `AGENTS.md`, ensuring that agents’ descriptions stay current with the latest changes.

### Build & Test Commands
```bash
# Install dependencies
uv sync

# Create distribution artifacts (if needed)
uv build

# Run documentation generator
uv run python3 docgen/docgen.py
```
Testing is performed via:
```bash
uv run pytest tests/ -v --tb=short          # Python unit tests with coverage and mocks
npm test                                    # JavaScript tests
go test ./...                                # Go package tests
```

### Dependencies
- **Python**: `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`
- **Linting**: Code style and quality are enforced with the `ruff` linter.

### Why This Matters for AI Agents
By automating test execution, documentation generation, and agent description updates on every commit, agents built from this repository can reliably consume accurate metadata without manual intervention. The pipeline ensures that any change in functionality is reflected both in tests (catching regressions) and in the human‑readable docs used by other tools or developers interacting with the AI system.
**使用技術**: python, shell


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
 │  │  ├─ javascript_detector.py
 │  │  └─ plugin_registry.py
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-28 16:19:39*