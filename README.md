# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
agents-docs-sync は、コミットごとに自動的にテストを実行し、最新のドキュメントを生成して `AGENTS.md` を更新する CI/CD パイプラインです。  
主な機能は以下の通り：

- **Python と Shell のスクリプト** で構成されており、複数言語にまたがるプロジェクトでも一貫したビルド・テストを実現します。
- `uv` を利用して依存関係管理と環境構築（`uv sync`, `uv build`) が行われます。  
  - **Python**: pyyaml≥6.0.3, pytest≥7.4.0, pytest‑cov≥4.1.0, pytest-mock≥3.11.1
- ビルドステップは次の順序で実施されます：
  1. `uv sync` – 必要なパッケージをインストール  
  2. `uv build` – バイナリやビルド成果物を生成  
  3. `uv run python3 docgen/docgen.py` – ドキュメントの自動生成と `AGENTS.md` の更新
- テスト実行は多言語対応で、以下コマンドが走ります：
  - Python: `uv run pytest tests/ -v --tb=short`
  - Node.js: `npm test`
  - Go: `go test ./...`
- コーディング規約として **ruff** を使用し、コード品質と整合性を保ちます。

### 利用フロー
1. プロジェクトに変更をコミット  
2. CI が自動でビルド・テスト → ドキュメント生成 & `AGENTS.md` 更新  
3. 失敗時はログが出力され、修正後再度プッシュ

この仕組みにより、最新の API 情報や設定手順を常に反映した README とマニュアルを維持でき、開発者間で情報共有がスムーズになります。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 18:38:33*