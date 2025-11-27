# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
The **agents-docs-sync** repository implements an automated workflow that keeps the project’s documentation in sync with its source code whenever changes are committed.  
Key features include:

* **Automated testing** – every commit triggers a full test suite covering Python, JavaScript and Go components to guarantee backward‑compatibility across all languages.
* **Dynamic documentation generation** – after tests pass, `docgen/docgen.py` runs against the repository’s source files (Python modules, YAML agent definitions, etc.) to rebuild API reference pages in Markdown format.  
  The generated docs are then committed back into the repo as part of the same pipeline run.
* **AGENTS.md maintenance** – a dedicated script scans all agent configuration files and rewrites `AGENTS.md` with an up‑to‑date table that lists each agent’s name, description, required parameters and status.  
  This removes manual effort and eliminates stale entries in the documentation.

## Development environment

The project is written primarily in **Python** (≥ 3.12) with supporting shell scripts for orchestration:

```bash
# Install dependencies via uv
uv sync          # resolves pyproject.toml, installs pyyaml, pytest, etc.
```

### Build process

1. `uv build` – builds a distributable wheel of the package.  
2. `uv run python3 docgen/docgen.py` – regenerates all Markdown documentation and updates `AGENTS.md`.

The resulting artifacts are committed automatically by the CI pipeline.

## Testing strategy

Tests cover three language ecosystems:

| Language | Test command |
|----------|--------------|
| Python   | `uv run pytest tests/ -v --tb=short` (with coverage & mocks) |
| JavaScript | `npm test` – runs Jest or Mocha suites defined in the repo’s package.json |
| Go       | `go test ./...` – executes all unit and integration tests across modules |

All tests are executed sequentially on each push, ensuring that any change does not break existing functionality.

## Coding standards

The repository enforces a strict linting policy using **ruff**:

```bash
# Run the linter before committing changes
uv run ruff check .
```

This guarantees consistent formatting and helps catch common Python errors early in development.

---

By integrating testing, documentation generation and agent list maintenance into a single CI pipeline, `agents-docs-sync` eliminates manual updates, reduces human error, and ensures that both developers and end‑users always see accurate, up‑to‑date information about every available agent.

## 使用技術

- Python
- Shell

## 依存関係

- **Python**: `pyproject.toml` または `requirements.txt` を参照

## セットアップ


## 前提条件

- Python 3.12以上



## インストール


### Python

```bash
# uvを使用する場合
uv sync
```




## LLM環境のセットアップ

### APIを使用する場合

1. **APIキーの取得と設定**

   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください




## ビルドおよびテスト

### ビルド

```bash
uv sync
uv build
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```



---

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 23:23:51*