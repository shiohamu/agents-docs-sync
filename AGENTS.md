# AGENTS ドキュメント

自動生成日時: 2025-11-27 09:52:59

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


This repository implements an automated pipeline that keeps the **AGENTS.md** file in sync with the rest of your project whenever you push a commit.  
The workflow is deliberately lightweight so it can be run locally or integrated into any CI/CD system without modification.

- **Trigger** – Each `git push` (or manual invocation) starts the sequence.
  - The pipeline first runs unit tests across all supported languages (`python`, `nodejs`, and `go`) to guarantee that new changes do not break existing functionality.
  - If all tests pass, it proceeds to generate fresh documentation from source files using a custom Python script located at **docgen/docgen.py**.  
    The generated output is placed in the repository’s docs directory and merged into AGENTS.md via templated placeholders.

- **Key commands**
  ```bash
  # Resolve dependencies with uv (the modern replacement for pip/poetry)
  uv sync

  # Build any compiled artifacts required by tests or doc generation
  uv build

  # Generate documentation & update the agents manifest
  uv run python3 docgen/docgen.py
  ```

- **Testing** – The pipeline runs three distinct test suites to cover all languages:
  ```bash
  uv run pytest tests/ -v --tb=short          # Python unit tests (pytest, coverage)
  npm test                                   # JavaScript / Node.js tests
  go test ./...                               # Go language tests
  ```
  All failures abort the pipeline; only when every suite passes does the documentation step execute.

- **Dependencies**
  *Python*:  
    - `pyyaml>=6.0.3` – YAML parsing for configuration files and metadata extraction.  
    - `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` – Robust testing utilities with coverage reporting.  

  *Other tooling* – The repository also contains a minimal Node.js test harness (`npm test`) and Go tests; these require the corresponding runtime environments but no external Python packages.

- **Coding style**  
  All source files are linted by `ruff`, ensuring consistent formatting, unused import detection, and other static checks. Running:
  ```bash
  uv run ruff check .
  ```
  will surface any violations before committing changes.

- **Output format – AGENTS.md**  
  The generated file follows a strict Markdown schema that AI agents can parse unambiguously: each agent section contains an `id`, `description`, and a list of supported actions. A minimal example:
  The script guarantees that every agent documented in code is represented, and any removed agents are pruned automatically.

- **Extensibility**  
  To add support for another language or new documentation format:
  1. Extend the `docgen/docgen.py` parser to discover entities.
  2. Update the test suite accordingly.
  3. Add a corresponding build/test command in the pipeline section above.

By keeping AGENTS.md up‑to‑date automatically, this project removes manual bookkeeping from developers and provides AI agents with an accurate, machine‑readable knowledge base of all available capabilities at any point in time.
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 09:52:59*