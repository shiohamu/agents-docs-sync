# agents-docs-sync

<!-- MANUAL_START:description -->
コミットするごとにテスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン
<!-- MANUAL_END:description -->

## 使用技術

- Python
- Shell

## 依存関係

### Python
- anthropic>=0.74.1
- httpx>=0.28.1
- jinja2>=3.1.0
- openai>=2.8.1
- outlines>=1.2.8
- pydantic>=2.0.0
- pytest>=9.0.1
- pyyaml>=6.0.3

## セットアップ

<!-- MANUAL_START:setup -->
# Setup


## Prerequisites

- Python 3.12以上



## Installation


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
<!-- MANUAL_END:setup -->



## ビルドおよびテスト


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

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 17:13:11*

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 17:13:11*