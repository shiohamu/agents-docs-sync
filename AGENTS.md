# AGENTS ドキュメント

自動生成日時: 2025-11-29 11:36:31

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents‑docs‑sync は、エージェントの設定ファイル（YAML/JSON）から自動的に Markdown 形式のドキュメントを生成し、それらを指定したリポジトリへ同期する CLI ツールです。  
Python とシェルスクリプトで構成されており、以下のようなアーキテクチャと機能が特徴です。

### アーキテクチャ

```
┌───────────────────────┐
│   システムレベル       │  (ユーザー・CI/CD パイプライン)
├────────────┬──────────┤
│ CLI（agents‑docs-sync） │  ← pyproject.toml の `scripts` によりエントリポイントを登録
│ └─ main() → docgen.docgen:main   │
├───────────────────────┤
│ Python ランタイム     │
│ ├─ docgen/          │  ドキュメント生成ロジック（Markdown・HTML）
│ │ ├─ models.py      │  Pydantic ベースの `AgentsConfig` モデルで設定を検証
│ │ └─ generator.py   │  設定からテンプレートへ変換し、ファイルを書き出す
│ └─ utils/           │  ファイル操作・Git 操作（シェルラッパー）  
├───────────────────────┤
│ システムツール       │ (git, rsync 等)
└───────────────────────┘
```

- **CLI**: `agents-docs-sync --help` でオプション一覧を確認でき、ドキュメント生成・同期のフローをスクリプト化。
- **Python モジュール**:
  - `docgen.models.agents.AgentsConfig`: エージェント設定ファイル（例: agents.yaml）を読み込み検証。  
  - `docgen.generator.generate_docs()`: 設定から Markdown を生成し、`docs/agents/` に出力。
- **同期**:
  - Git リポジトリへのコミット・プッシュはシェルコマンド（git, rsync）を呼び出すことで実現。  
  - `--dry-run` オプションで変更点のみ表示し、事前確認が可能。

### 主な機能

- **設定から自動生成**: エージェントごとの説明・パラメータ一覧をテンプレート化して Markdown に変換。
- **差分同期**: 既存のドキュメントと比較し変更箇所のみ更新。CI/CD パイプラインで `--no-push` を指定すればローカルだけに残せる。
- **汎用性の高いエントリポイント**:
  - 複数名前（`agents-docs-sync`, `agents_docs_sync`）を登録し、スクリプトから直接呼び出せます。  
  - シェルラッパー (`scripts/`) を追加すれば、Windows のバッチファイルや Unix のシェルで簡単に利用可能。
- **拡張性**: `docgen.generator` はテンプレートエンジン（Jinja2）を使用しているため、新しいドキュメントフォーマットへの対応も容易。

### 利用例

```bash
# ドキュメント生成と同期 (デフォルト)
agents-docs-sync --config agents.yaml --target docs/agents/

# 変更点だけ表示（プッシュはしない）
agents-docs-sync --dry-run

# CI 用の簡易スクリプト
export AGENTS_CONFIG=ci/config.yml
agents-docs-sync -c $AGENTS_CONFIG -t /tmp/docs/
```

### 開発・テスト環境

- **Python 3.10+**  
- `pip install .` でインストール可能。pyproject.toml の `[tool.poetry.dependencies]`（または PEP 621）に必要ライブラリが列挙されています。
- テストケース (`tests/`) は PyTest を利用し、生成結果と Git 操作のモックを行います。

agents‑docs‑sync はエージェントドキュメント管理を自動化することで、手入力ミスや更新漏れを防ぎます。プロジェクト内で共通設定を一元化したい場合はもちろん、複数リポジトリに同じフォーマットのドキュメントを保管したいケースにも最適です。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-29 11:36:31*