# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
agents-docs-sync は、Python とシェルスクリプトによる自動化された CI パイプラインであり、コードベースにコミットがあるたびに以下を実行します。  

- **テストの走査**：Pytest（`pytest`, `pytest-cov`, `pytest-mock`）と他言語のユニットテスト (`npm test`, `go test ./...`) を同時に起動し、コード品質を保証  
- **ドキュメント生成**：Python スクリプト(`docgen/docgen.py`) が実行されて API ドキュメントや利用例などが自動的に更新  
- **AGENTS.md の同期**：最新のテスト結果とドキュメント内容をもとに `AGENTS.md` を再生成し、プロジェクト全体の情報整合性を保つ  

## 主な技術スタック

| 言語 | 主要パッケージ |
|------|----------------|
| Python | `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` |
| Shell | ビルド・実行スクリプト用 |

## 依存関係

- **Python**  
  - `pyyaml`: YAML ファイルの読み書き（設定やメタデータ管理）  
  - `pytest`, `pytest-cov`, `pytest-mock`: テストフレームワークとカバレッジ測定、モックライブラリ  

## ビルド手順

1. **依存パッケージの同期** – `uv sync`  
2. **ビルド実行** – `uv build`（必要に応じてコンテナ化や静的解析を含む）  
3. **ドキュメント生成スクリプト起動** – `uv run python3 docgen/docgen.py`

## テスト手順

- Python の単体/統合テスト: `uv run pytest tests/ -v --tb=short`  
- Node.js 関連のテスト（必要に応じて）: `npm test`  
- Go 言語のユニットテスト: `go test ./...`

## コーディング規約

- **リンタ**：`ruff` を使用して PEP8 互換性と静的解析を実施。CI パイプライン内で自動チェックが行われ、問題箇所はコミット前に修正される。

---

### 利点・期待効果
* コミットごとの**即時フィードバック**：テスト失敗やドキュメントの不整合を早期検知  
* **一貫した文書管理**：手動更新によるヒューマンエラーを排除し、最新情報が常に `AGENTS.md` に反映  
* 開発者は「ビルド・テスト」だけでなく、「ドキュメントの整合性」を同時に担保できるため、リリースサイクル短縮と品質向上を実現  

このパイプラインをプロジェクト全体へ統合することで、コードベースが拡張されても自動化されたワークフローで安定した成果物を継続的に提供できます。
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

*このREADME.mdは自動生成されています。最終更新: 2025-11-25 19:08:38*