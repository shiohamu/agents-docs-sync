# AGENTS ドキュメント

自動生成日時: 2025-11-26 05:28:03

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

This repository implements an automated documentation sync system named **agents-docs-sync** that keeps the `AGENTS.md` file in lockstep with your codebase and test suite. Every time a commit lands on any branch (or via CI), it triggers a sequence of actions:

1. **Dependency resolution** – Uses *uv* to install all required Python packages (`pyyaml`, `pytest`, etc.) ensuring the environment matches the declared constraints.
2. **Build & packaging** – Executes `uv build` so that your package can be installed in editable mode if needed, and verifies metadata consistency with PyPI standards.
3. **Documentation generation** – Runs a custom script located at `docgen/docgen.py`. This script parses YAML configuration files for each agent, extracts docstrings from the source code, and compiles them into Markdown snippets that are merged into `AGENTS.md`.
4. **Testing matrix** – The pipeline runs tests in three ecosystems to guarantee cross‑language compatibility:
   - Python: `uv run pytest tests/ -v --tb=short` (with coverage via `pytest-cov`)
   - Node.js: `npm test`
   - Go: `go test ./...`

5. **Linting** – Before committing the updated documentation, the codebase is linted with *ruff* to enforce PEP‑8 style guidelines and catch common syntax issues.

6. **Commit & push** – After successful build, tests, and linter pass, a new commit containing the regenerated `AGENTS.md` (and any auxiliary docs) is automatically pushed back to the repository, ensuring that documentation never falls out of sync with implementation changes.

### How it works for AI agents

- Each agent’s configuration resides in YAML files under `/agents/`. The generator parses these files and embeds them into a consistent table format within `AGENTS.md`.
- Docstrings from Python modules are extracted using introspection, enabling the documentation to reflect real‑time API signatures without manual updates.
- By integrating with CI (GitHub Actions / GitLab), any push triggers this pipeline; agents can also invoke it locally via the provided shell scripts.

### Usage

```bash
# Install uv if not already present:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run full sync manually:
uv sync          # install dependencies
uv build         # prepare package
uv run python3 docgen/docgen.py  # generate docs
```

Running the tests and linter is optional but recommended:

```bash
uv run pytest tests/ -v --tb=short   # Python unit tests
npm test                              # JavaScript tests
go test ./...                         # Go tests

ruff check .                           # Linting pass/fail
```

The repository’s CI configuration automatically performs these steps, so contributors only need to commit changes; the pipeline takes care of updating documentation and ensuring quality.

## 概要

コミットするごとにテスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン

**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
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
<!-- MANUAL_END:setup -->

---

## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順


['uv sync', 'uv build', 'uv run python3 docgen/docgen.py']


### テスト実行



#### APIを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
npm test
```

#### ローカルLLMを使用する場合

```bash
npm test
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
go test ./...
```

#### ローカルLLMを使用する場合

```bash
go test ./...
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。
<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->
### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```
<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:pr -->
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
<!-- MANUAL_END:pr -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-26 05:28:03*