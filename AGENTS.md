# AGENTS ドキュメント

自動生成日時: 2025-11-28 10:13:08

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


The **agents-docs-sync** pipeline is designed to keep the documentation of all AI agents in sync with their source code and test suite automatically whenever a commit is pushed to the repository.  

- **Trigger & Workflow**  
  * Every push initiates a CI job that runs three distinct phases: (1) dependency resolution (`uv sync`), (2) build artifacts creation (`uv build`), and (3) documentation generation via `python3 docgen/docgen.py`. The generated Markdown is then merged into the central **AGENTS.md** file, ensuring it reflects the latest agent definitions.  

- **Core Functionality**  
  * `docgen/docgen.py` scans the repository for Python modules, shell scripts and other language-specific files that expose an agent interface (decorators or naming conventions). It extracts metadata such as name, description, input/output schema, and example usage, then composes a Markdown section per agent.  

- **Testing & Validation**  
  * The pipeline verifies code quality through `uv run pytest` for Python tests with coverage (`pytest-cov`) and mocking support (`pytest-mock`). It also runs cross‑language checks: `npm test` validates any JavaScript/TypeScript tooling, while `go test ./...` ensures Go components compile and pass their unit tests.  

- **Dependencies & Environment**  
  * The project relies on the following Python packages (installed via UV):  
    - `pyyaml>=6.0.3`: for parsing YAML configuration files that may contain agent metadata.  
    - `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` : comprehensive test framework and coverage reporting.  
  * Code style enforcement is handled by the **ruff** linter, ensuring consistent formatting across all Python source files.  

- **Usage Instructions for Contributors**  
  1. Install UV (if not already installed).  
     ```bash
     uv venv create .venv --python=3.x   # optional virtual environment creation
     ```
  2. Sync dependencies: `uv sync`.  
  3. Build the project artifacts: `uv build`.  
  4. Generate or update documentation locally to preview changes: `uv run python3 docgen/docgen.py`.  
  5. Run tests before committing: 
     ```bash
     uv run pytest tests/ -v --tb=short
     npm test          # if the repository contains NodeJS components
     go test ./...      # for Go modules
     ```
  6. Commit changes; CI will automatically re‑run the pipeline and update **AGENTS.md**.

- **Key Benefits**  
  * Guarantees that `AGENTS.md` always reflects the current state of each agent, reducing manual documentation drift.  
  * Provides a single source of truth for both code behavior (tests) and user-facing description (docs).  
  * Supports multi‑language projects by integrating Python, JavaScript/TypeScript, and Go testing workflows within one cohesive pipeline.

This overview equips AI agents developers with the necessary context to understand how documentation stays current, what tools are involved, and how they can contribute safely without breaking the automated sync process.
**使用技術**: python, shell


## プロジェクト構造
```
agents-docs-sync/
 ├─ docgen/
 │  ├─ collectors/
 │  │  ├─ collector_utils.py
 │  │  └─ project_info_collector.py
 │  ├─ detectors/
 │  │  ├─ base_detector.py
 │  │  ├─ detector_patterns.py
 │  │  └─ javascript_detector.py
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-28 10:13:08*