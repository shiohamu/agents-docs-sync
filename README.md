# agents-docs-sync

<!-- MANUAL_START:description -->
コミットするごとにテスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン
<!-- MANUAL_END:description -->

## Technologies Used

- Python
- Shell

## Dependencies

### Python
- anthropic>=0.74.1
- httpx>=0.28.1
- jinja2>=3.1.0
- openai>=2.8.1
- outlines>=1.2.8
- pydantic>=2.0.0
- pytest>=9.0.1
- pyyaml>=6.0.3

## Setup

<!-- MANUAL_START:setup -->
# Setup


## Prerequisites

- Python 3.8以上



## Installation


### Python

```bash
# uvを使用する場合
uv venv
source .venv/bin/activate  # Linux/macOS
uv pip install -e .
```





<!-- MANUAL_END:setup -->




## Build and Test


### ビルド

```bash
uv run python3 docgen/docgen.py
```



### テスト

```bash
uv run pytest
npm test
uv run pytest tests/ -v --tb=short
```





---

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 14:30:42*