# AGENTS ドキュメント

自動生成日時: 2025-11-29 21:28:34

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、Python とシェルスクリプトで構築された軽量なドキュメント同期ツールです。  
CLI から `--help` を実行すると使用方法が表示されるように設計されています（例：`agents-docs-sync --help`）。  

### アーキテクチャ
```
┌───────────────────────┐
│          CLI           │   ← entrypoint (docgen.docgen:main)
├─────────────▲───────────┤
│             │           │
│  config.yml ─► ConfigParser（pydantic / dataclass）  
│            │           │
│    Models (AgentsConfig, AgentsGenerationConfig,
│     AgentsDocument …)   │
│            ▼           │
│      DocGenerator          │ ← AGENTS.md 等を生成・同期
└───────────────────────┘
```
- **CLI**: `pyproject.toml` の `[project.scripts]` により、インストール後はシステム PATH から直接呼び出せるスクリプトが作成されます。  
- **設定モデル** (`docgen/models/agents.py`) は Pydantic クラスで構築されており、JSON/YAML 設定ファイルを型安全に読み込みます。主なクラスは `AgentsConfig`, `AgentsGenerationConfig`, `AgentsDocument` です。  
- **ドキュメント生成**: 設定情報とソースコードのメタデータ（例えば docstring やコメント）から、統一フォーマットの AGENTS.md を自動で作成します。既存ファイルとの差分検出も行い、必要な箇所だけを書き換えることで同期を保ちます。

### 主機能
- **構造化設定**: YAML/JSON 形式の `agents.yml`（または `.json`) による詳細設定。  
- **自動ドキュメント生成**: コードベースから必要情報を抽出し、Markdown 文書へ変換。  
- **差分同期**: ファイル変更時にのみ更新され、不必要なリライトを防止します。  
- **CLI ユーティリティ**: `--help` でオプション一覧表示。その他のフラグ（例：`--dry-run`, `--output-dir`）も実装予定です。

### 技術スタック
| レイヤー | 実装技術 |
|----------|---------|
| CLI      | Python (docgen.docgen:main) + シェルスクリプトラッパー |
| 設定解析 | Pydantic / dataclass（型安全な設定モデル） |
| ドキュメント生成 | Markdown テンプレートエンジン、ファイル差分検出アルゴリズム |
| パッケージ管理 | `pyproject.toml` (PEP 621) |

### 開発フロー
1. リポジトリをクローン  
   ```bash
   git clone https://github.com/your-org/agents-docs-sync.git
   cd agents-docs-sync
   ```
2. 必要に応じて `pip install .` でローカルインストール。  
3. 設定ファイルを編集し、`agents-docs-sync --help` を実行して確認。  

このツールはドキュメントの整合性と保守コスト削減を目的としており、大規模プロジェクトでもスムーズに導入できます。
**使用技術**: shell, python


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
 │  │  ├─ detector_patterns.py
 │  │  ├─ plugin_registry.py
 │  │  └─ unified_detector.py
 │  ├─ generators/
 │  │  ├─ mixins/
 │  │  │  ├─ llm_mixin.py
 │  │  │  ├─ markdown_mixin.py
 │  │  │  └─ template_mixin.py
 │  │  ├─ parsers/
 │  │  │  ├─ base_parser.py
 │  │  │  ├─ generic_parser.py
 │  │  │  ├─ js_parser.py
 │  │  │  └─ python_parser.py
 │  │  ├─ agents_generator.py
 │  │  ├─ api_generator.py
 │  │  ├─ base_generator.py
 │  │  ├─ contributing_generator.py
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
 │  │  ├─ config.py
 │  │  └─ detector.py
 │  ├─ prompts/
 │  │  ├─ agents_prompts.toml
 │  │  ├─ commit_message_prompts.toml
 │  │  └─ readme_prompts.toml
 │  ├─ rag/
 │  │  ├─ embedder.py
 │  │  ├─ indexer.py
 │  │  ├─ retriever.py
 │  │  └─ validator.py
 │  ├─ utils/
 │  │  ├─ llm/
 │  │  │  ├─ base.py
 │  │  │  └─ local_client.py
 │  │  ├─ cache.py
 │  │  ├─ exceptions.py
 │  │  ├─ file_utils.py
 │  │  └─ prompt_loader.py
 │  ├─ config.toml
 │  ├─ config_manager.py
 │  ├─ docgen.py
 │  └─ hooks.toml
 ├─ docs/
 ├─ scripts/
 ├─ tests/
 ├─ AGENTS.md
 ├─ README.md
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 21:28:34*