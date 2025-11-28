# AGENTS ドキュメント

自動生成日時: 2025-11-29 06:22:47

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


Python とシェルスクリプトで構築された **agents‑docs‑sync** は、コミットごとに自動的にテスト実行・ドキュメント生成・AGENTS.md の更新を一括して処理するパイプラインです。  
以下はその技術設計と主な機能の概要です。

### アーキテクチャ

| 層 | 主体 | 役割 |
|---|------|-----|
| **CLI** | `docgen.docgen:main`（エントリポイント） | コマンドライン引数をパースし、実行フローを制御。`agents-docs-sync --help` によって利用方法が表示されます。 |
| **ビルドロジック** | `docgen.build` モジュール群 | ① テスト（pytest） → ② ドキュメント生成（MkDocs/Sphinx） → ③ AGENTS.md 更新を順次実行。各ステップは例外時にログを書き、失敗したら以降の処理をスキップします。 |
| **モデル** | `docgen.models.agents.AgentsConfig` | Pydantic を用いた構成データクラスで、エージェント情報（名前・バージョン・説明）を定義し、Markdown へシリアライズするロジックが実装されています。 |
| **ファイルIO** | `docgen.io` モジュール | ソースコードの変更検知と AGENTS.md の差分更新を行います。Git のハッシュ情報も埋め込み可能です。 |

### 主な機能

- **自動テスト実行**
  - コミット時に `pytest --maxfail=1` を呼び出し、失敗した場合は即座にビルドを中断。
  - テスト結果は標準出力とログファイルに保存。

- **ドキュメント生成**
  - MkDocs（または Sphinx）で `docs/` ディレクトリ内の Markdown を HTML に変換し、`site/` フォルダへ配置。
  - ビルド前後にバージョン番号やコミットハッシュを埋め込み。

- **AGENTS.md の自動更新**
  - `AgentsConfig` モデルからエージェント一覧を抽出し、Markdown テーブルとして再生成。
  - 差分のみを書き込むことで大規模リポジトリでも高速に実行可能。

- **CLI オプション**  
  ```bash
  agents-docs-sync --help          # ヘルプ表示
  agents-docs-sync --skip-tests    # テストをスキップしてビルドのみ
  agents-docs-sync --output-dir DIR# 出力先ディレクトリの指定
  ```

- **CI/CD 統合**  
  - GitHub Actions のワークフローで `pre-commit` フックに組み込み、プッシュ前に自動実行。
  - 成功時は生成されたサイトを `gh-pages` ブランチへデプロイ。

### 技術的ハイライト

| 要素 | 詳細 |
|------|-----|
| **パッケージ管理** | Poetry（pyproject.toml）で依存関係 (`click`, `pydantic`, `pytest`, `mkdocs`) を宣言。スクリプトエントリポイントは `[project.scripts]` に設定されています。 |
| **テストフレームワーク** | Pytest でユニット・インテグレーションテストを網羅し、CI の品質保証に利用。 |
| **ドキュメント生成ツール** | MkDocs（テーマ: Material）または Sphinx を選択可能。設定ファイル (`mkdocs.yml` / `conf.py`) はリポジトリルートで管理されます。 |
| **コード構造** | モジュール化された設計により、各ステップを独立してテスト・デバッグが容易です。 |

### 使い方の流れ

1. コミット前に `git add .` → `git commit -m "msg"`  
2. CI が起動し、**agents‑docs‑sync** パイプライン実行  
3. テスト失敗時はコミットを中断（エラーメッセージで詳細表示）  
4. 成功したらドキュメント生成 → AGENTS.md 更新  
5. `gh-pages` へ自動デプロイ完了

### メリットまとめ

- **一貫性**：テスト・ドキュメント・設定ファイルが常に同期。  
- **高速化**：差分更新と並列実行でビルド時間を短縮。  
- **保守容易**：Python モジュール単位の設計で拡張や修正が楽々。  

このパイプラインは、エージェント駆動型プロジェクトにおいて開発フローと文書化の両立を実現し、生産性向上へ直接貢献します。
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
 │  │  ├─ chunker.py
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
 ├─ PROJECT_MANAGEMENT_GUIDE.md
 ├─ README.md
 ├─ RELEASE.md
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 06:22:47*