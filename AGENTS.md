# AGENTS ドキュメント

自動生成日時: 2025-11-29 06:13:06

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


`agents-docs-sync` は、ソースコードのコミットごとに自動でテスト実行・ドキュメント生成・AGENTS.md 更新を行うパイプラインです。  
Python 3.x（typing, pathlib 等）＋シェルスクリプトで構成されており、CLI エントリポイントは `pyproject.toml` の `[project.scripts]` に

```toml
agents-docs-sync = "docgen.docgen:main"
```

として登録されています。  

## アーキテクチャ  
- **コマンドラインインターフェース** – `python -m docgen.docgen` を実行すると、以下のフローが順に走ります。  
  1. **テストランナー**：`pytest --cov=docgen tests/` によりユニット・統合テストを実施し、失敗時は即座に停止します。  
  2. **ドキュメント生成** – `pydoc-markdown`／Sphinx を利用してモジュールの docstring と型ヒントから Markdown/HTML ドキュメント (`docs/api/*.md`) を作成。  
  3. **AGENTS.md 自動更新** – ソース内に定義された Agent クラス（@agent デコレータ付き）をリフレクションで走査し、名前・概要・パラメーター一覧を YAML/JSON として抽出後、`templates/agencies.tmpl.j2` を Jinja でレンダリング。  

- **CI/CD パイプライン** – GitHub Actions の `ci.yml` がブランチへの push 時にトリガされます。  
  - ランタイム環境は Ubuntu 最新版、Python 3.12 を使用。  
  - コード品質チェック（flake8, mypy）とセキュリティスキャン (bandit) も併せて実行します。

## 主な機能  

| 機能 | 説明 |
|------|-------|
| **自動テスト** | `pytest` + coverage を統合し、コード変更ごとの回帰検証を保証。 |
| **ドキュメント生成** | すべてのモジュールとクラスに対して Markdown（HTML）形式で最新状態を維持。Sphinx の autodoc と pydoc-markdown が併用されるため、型ヒントも含めた詳細な API ドキュメントが取得可能。 |
| **AGENTS.md 更新** | 変更された Agent 定義に応じて自動的に `AGENTS.md` を再生成し、README 等で最新のエージェント一覧を即時反映。 |
| **CLI オプション** | `--no-tests`, `--only-docs`, `--dry-run` などで実行粒度を制御可能。 |
| **拡張性** | 新しいドキュメントフォーマット（例：OpenAPI スペック）やテストフレームワークへの切替が容易にできるよう、プラグインベースの設計を採用。 |

## 技術的ハイライト  

- **型安全性**: `typing` と `pydantic` を併用し、実行時入力検証も行う。  
- **テストカバレッジ 100% 近辺**（coverage.io により可視化）。  
- **CI の高速化**: キャッシュ機構に Docker layers / pipenv lockfile を利用してビルド時間を短縮。  
- **セキュリティ対策**: `bandit` と `safety` で依存関係の脆弱性チェック、静的解析時に未使用コードや潜在バグも検出。

## 今後の拡張予定  

1. **パフォーマンスベンチマーク**：テスト実行時間を可視化しボトルネック特定。  
2. **CI パイプラインへの品質ゲート追加**：flake8、mypy のスコアに応じてブランクリリースを防止。  
3. **コード監査の自動実行**：GitHub Security Advisories と連携し脆弱性情報を即時取得。

`agents-docs-sync` は CI で走る一連のタスクを統括することで、エンジニアは「テストとドキュメントが常に最新」な状態を手間なく維持できるよう設計されています。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 06:13:06*