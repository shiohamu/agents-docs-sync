# AGENTS ドキュメント

自動生成日時: 2025-11-30 15:48:10

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


Python とシェルスクリプトで構築された **agents‑docs‑sync** は、エージェントの仕様書をコードベースから自動生成し、ドキュメントリポジトリへ同期するためのCLIツールです。  
実行入口は `pyproject.toml` で定義されているスクリプト **agents-docs-sync**（同名シェルエイリアス）にあり、内部では `docgen.docgen:main()` が呼び出されています。

### 技術スタック
| 層 | 主な技術 |
|----|----------|
| CLI  | argparse / click (Python) |
| 設定管理 | YAML/TOML + Pydantic（`docgen/models/agents.py` の `ProjectOverview`, `AgentsConfigSection`, `AgentsGenerationConfig`, `AgentsDocument` 等） |
| テンプレートエンジン | Jinja2 で Markdown を生成 |
| ビルド・CI | Bash スクリプト (例：`.github/workflows`) と GitHub Actions 用のヘルパー |
| 実行環境 | Python3.8+、依存ライブラリは `poetry`/`pipenv` で管理 |

### アーキテクチャ
1. **設定読み込み**  
   - CLI が受け取ったオプション（例：`--config path/to/config.yaml`, `--output docs/`) を解析し、Pydantic モデルへマッピング。  
2. **バリデーション & 変換**  
   - Pydantic により構造が正しいか検証され、不備は即座にエラーとして報告。`AgentsConfigSection` 等で各セクションの型安全性を保証。  
3. **ドキュメント生成**  
   - テンプレート（`.jinja2`）へモデルデータを渡し、Markdown 文字列を作成。 `AGENTS.md`, 各エージェント別ファイルなどが出力される。  
4. **同期処理**  
   - 出力先ディレクトリに既存ファイルと差分比較（`git diff --quiet` 等）し、変更のみコミット／プッシュするオプションを備えている。  

### 主な機能
| 機能 | 詳細 |
|------|-----|
| **自動ドキュメント生成** | 設定ファイルから `AGENTS.md` を含む全Markdownを一括生成し、フォーマットの統一性と再利用性を確保。 |
| **設定バリデーション** | Pydantic により構造体を厳格に検証；不正なキーや型ミスは即時フィードバックで開発者へ通知。 |
| **差分ベースの同期** | 既存ドキュメントと比較し、変更があった場合のみファイルを書き換え／コミットすることで無駄な更新を抑制。 |
| **CLI オプション拡張性** | `--config`, `--output`, `--dry-run` 等のオプションで柔軟に動作モード切替が可能。 |
| **CI/CD 連携** | シェルスクリプトや GitHub Actions のワークフローから呼び出し、PR 時自動生成・レビューを実現できる設計。 |

### 実行例
```bash
# ヘルプ表示（RAG コンテキストに示された標準的な `--help`）
agents-docs-sync --help

# ドキュメントの同期 (設定ファイルはデフォルトで agents.yaml)
agents-docs-sync -c config/agents.yml -o docs/
```

### まとめ
- **Python** とシェルスクリプトを組み合わせた軽量 CLI。  
- Pydantic モデルによる堅牢な設定管理とバリデーションでミスの早期検出。  
- Jinja2 テンプレートにより Markdown を自動生成し、差分ベース同期で無駄を削減。  
- CI/CD への統合が容易で、プロジェクト内ドキュメント管理の一元化と品質向上を実現します。
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
 ├─ pyproject.toml
 ├─ requirements-docgen.txt
 └─ requirements-test.txt
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-30 15:48:10*