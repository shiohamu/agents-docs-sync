# agents-docs-sync

<!-- MANUAL_START:description -->
## Overview

This project, **agents-docs-sync**, provides a lightweight CI/CD pipeline that automates documentation generation and synchronization for AI coding agents.

**Key Features**:
- **Automated Test Execution**: Runs tests using Python (`pytest`) or JavaScript test automation
- **Documentation Auto-Sync**: Automatically updates `AGENTS.md` and `README.md` based on code changes
- **GitHub Actions Integration**: Triggers automated workflows on push events
- **LLM Support**: Works with both local LLM (LM Studio, Ollama) and API-based LLM (OpenAI, Anthropic)

**Workflow**:
1. Detects new commits via GitHub Actions triggers
2. Runs automated tests to ensure code quality
3. Updates `AGENTS.md` with current project information and agent specifications
4. Synchronizes documentation with codebase changes

The pipeline ensures that documentation stays up-to-date with minimal manual intervention, making it easier for AI coding agents to understand and work with the project.
<!-- MANUAL_END:description -->

## 使用技術

- Python
- JavaScript
- Shell

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.8以上
- Node.js 14以上

### インストール手順

```bash
# Pythonの依存関係をインストール
pip install -r requirements-docgen.txt
pip install -r requirements-test.txt

# Node.jsの依存関係をインストール (必要に応じて)
npm install
```

### LLM環境のセットアップ

#### ローカルLLMを使用する場合

1. **LM Studioのインストール**
   - [LM Studio](https://lmstudio.ai/)をダウンロードしてインストール
   - お好みのモデルをダウンロード
   - サーバーを起動（デフォルト: `http://localhost:1234`）

2. **設定ファイルの編集**
   - `docgen/config.yaml`を編集
   - `llm_mode`を`local`または`both`に設定
   - `local_llm`の`base_url`を確認

#### API LLMを使用する場合

1. **APIキーの設定**
   - 環境変数に APIキーを設定
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # または
   export ANTHROPIC_API_KEY="your-api-key"
   ```

2. **設定ファイルの編集**
   - `docgen/config.yaml`を編集
   - `llm_mode`を`api`または`both`に設定
   - 使用するプロバイダーとモデルを指定
<!-- MANUAL_END:setup -->

## プロジェクト構造

```
├── .github
│   └── workflows
├── agents_docs_sync
├── agents_docs_sync.egg-info
├── docgen
│   ├── detectors
│   ├── generators
│   ├── collectors
│   ├── hooks
│   └── templates
├── docs
│   └── implementation/
├── scripts
├── tests
│   ├── test_collectors
│   ├── test_detectors
│   ├── test_generators
│   └── test_parsers
├── AGENTS.md
├── README.md
...
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-18 12:49:56*
