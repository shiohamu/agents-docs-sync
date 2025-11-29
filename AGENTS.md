# AGENTS ドキュメント

自動生成日時: 2025-11-29 11:21:58

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


`agents-docs-sync` は、複数のリポジトリにまたがるエージェント定義（YAML/JSON など）を元に自動でドキュメントを生成・同期する CLI ツールです。  
Python とシンプルな Shell スクリプトから構成され、以下のようなアーキテクチャと機能が備わっています。

- **エントリポイント**  
  `pyproject.toml` の `[project.scripts]` に登録された
  ```text
  agents-docs-sync = "docgen.docgen:main"
  ```
  が実行され、コマンドラインオプションを解析して処理のフローを制御します。

- **設定モデル**  
  `AgentsConfig`（`docgen/models/agents.py`）は Pydantic ベースで定義され、
  エージェントごとのメタ情報・パラメータ構造・依存関係などを型安全に保持し、ドキュメント生成時の入力ソースとして使用します。

- **ドキュメントジェネレーター**  
  - Jinja2 テンプレートエンジンで Markdown／HTML を動的に作成
  - エージェントごとの API ドックや設定例を自動挿入
  - カスタムフィルタ・マクロによりフォーマットの拡張が可能

- **同期機能**  
  Git コミット／プッシュ操作を内部で呼び出し、生成したドキュメントを対象リポジトリへ自動反映します。  
  - `--dry-run` オプションで変更内容の差分だけ表示
  - CI/CD 環境向けに環境変数ベースの認証情報取得

- **Shell スクリプトラッパー**（`agents_docs_sync.sh` 等）  
  Windows/Unix 両方で動作するシェルスクリプトを用意し、Python の依存関係が整っていない環境でも簡易的に `--help` を表示可能。  
  - 環境変数チェック
  - 仮想環境の自動起動

- **主要コマンド**（例）  
  ```bash
  agents-docs-sync --config path/to/agents.yaml \
                   --output docs/agent_docs.md \
                   --repo https://github.com/example/repo.git
  ```
  * `--help`：利用可能オプション一覧を表示
  * `--verbose`：詳細ログ出力

- **テスト・CI**  
  - PyTest を用いたユニットテストが含まれ、GitHub Actions で毎コミット時にビルド＆テスト実行。
  - コードカバレッジは 90%+ を目指し、品質保証を徹底。

- **拡張性**  
  `docgen/templates/` ディレクトリ内のテンプレートファイルや設定により、新しいドキュメント形式（ReStructuredText, AsciiDoc 等）への追加も容易です。  

> このツールは、エージェント開発チームが共通フォーマットでドキュメントを管理しつつ、CI/CD パイプライン内から自動同期できるよう設計されており、大規模プロジェクトに最適化されています。
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
 │  │  ├─ agents_prompts.yaml
 │  │  ├─ commit_message_prompts.yaml
 │  │  └─ readme_prompts.yaml
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
 │  ├─ config.yaml
 │  ├─ config_manager.py
 │  ├─ docgen.py
 │  └─ hooks.yaml
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 11:21:58*