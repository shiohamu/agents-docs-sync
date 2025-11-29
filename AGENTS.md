# AGENTS ドキュメント

自動生成日時: 2025-11-29 19:11:36

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、エージェントに関するドキュメントを宣言的な設定ファイルから自動生成し、複数リポジトリやブランチ間で同期できる CLI ツールです。Python 3 とシンプルな Shell スクリプトの組み合わせで構築されており、`agents-docs-sync --help` のようにコマンドラインから直感的に操作できます。

### アーキテクチャ概要
- **CLI エントリポイント**： `pyproject.toml` に記載されたスクリプトエイリアン（`agents-docs-sync`, `agents_docs_sync`）は、`docgen.docgen:main` を呼び出します。  
- **設定モデル化**： `docgen/models/agents.py` で Pydantic ベースのクラス (`AgentsConfig`, `AgentsGenerationConfig`, `AgentsDocument`) が定義されており、YAML／JSON の構成ファイルを検証・パースして内部データ構造へ変換します。  
- **ドキュメント生成**： パーサが作ったモデルオブジェクトから Markdown（主に AGENTS.md） をテンプレートエンジンで組み立て、指定ディレクトリへ出力します。  
- **同期機能**： 生成したファイルを対象リポジトリの特定パスへコピー／コミットし、必要なら GitHub Actions 等に連携できるよう Shell スクリプトが用意されています。

### 主な機能
| 機能 | 内容 |
|------|------|
| **宣言的ドキュメント生成** | 設定ファイル一式でエージェントの概要・パラメータ・実装例を記述し、AGENTS.md を自動構築。 |
| **多リポジトリ同期** | 1 本の設定から複数プロジェクトへ同時にドキュメントを書き込むことが可能（Git コミット/プッシュは Shell スクリプトで実装）。 |
| **拡張性** | `docgen` パッケージ内のモジュールを追加・置換するだけで、独自フォーマットや出力先へ対応。 |
| **CI/CD 連携** | GitHub Actions 用 YAML が同梱されており、PR 時にドキュメントが最新になるよう設定できる。 |

### 技術スタック
- Python: `typing`, `dataclasses` (Pydantic), `click`（CLI）  
- Shell: Bash スクリプトで Git 操作・ファイルコピーを実行  
- パッケージ管理： Poetry による依存関係とビルド設定  

これらの要素が組み合わさり、エンジニアはコードを書き換えるだけでなく、機能追加や既存ドキュメント更新も高速に行えます。プロジェクト管理ガイド（`PROJECT_MANAGEMENT_GUIDE.md`）と設定ガイド (`CONFIG_GUIDE.md`) が揃っているため、新規導入時のハードルが低くなっています。
**使用技術**: python, shell


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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 19:11:36*