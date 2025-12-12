# agents-docs-sync

<!-- MANUAL_START:notice -->

<!-- MANUAL_END:notice -->


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
- **目的**  
  `agents-docs-sync` は、リポジトリへコミットが入るたびに自動で以下の処理を実行する CI パイプラインです。  

  | 処理 | 内容 |
  |------|-----|
  | テスト実行 | `pytest`, `pytest-cov`, `pytest-mock` を用いてユニットテストとカバレッジ測定を行う。 |
  | ドキュメント生成 | ソースコードから Markdown / HTML のドキュメント（例: MkDocs、Sphinx）へ変換し、最新の API リファレンスや使用方法を提供する。 |
  | AGENTS.md 自動更新 | プロジェクト内に定義されたエージェント情報を YAML 等で管理し、コミット時に `AGENTS.md` を再生成して常に最新状態に保つ。 |

- **構成**  
  - 言語: Python（3.11+）とシェルスクリプト
  - パッケージマネージャー: [uv](https://github.com/astral-sh/uv) を使用し、依存関係を高速に解決・インストール。  
    ```bash
    uv sync   # 必要なパッケージのインストール／更新
    ```
  - 主な Python ライブラリ（バージョン指定）: `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`  
    他のユーティリティやテストヘルパーも同様に uv で管理される。  

- **ワークフロー**  
  1. コミットがプッシュされると、GitHub Actions（または他 CI）から `ci/pipeline.sh` が起動。  
  2. スクリプト内で以下を順に実行:  
     - `uv sync --frozen`
     - `pytest tests/ --cov=src --cov-report xml`
     - ドキュメントビルド (`mkdocs build`, `sphinx-build` 等)
     - AGENTS.md 生成スクリプト（例: `scripts/gen_agents_md.py`)  
  3. 成功すれば成果物を GitHub に自動コミット／PRに反映、失敗した場合はログとエラー情報が通知される。  

- **メリット**  
  - コードベースの品質（テスト・カバレッジ）を常時確認でき、ドキュメントとのズレを防止。  
  - AGENTS.md の手動更新作業が不要になり、人為的ミスや忘れ漏れリスクを低減。  
  - `uv` による高速な依存解決で CI 実行時間の短縮に貢献。  

- **拡張性**  
  新しいテストフレームワーク、ドキュメントツール、またはエージェント情報フォーマットを追加したい場合も、スクリプトと YAML 定義ファイルを編集するだけで簡単に対応可能。  

- **利用例**  
  ```bash
  # 開発中のローカルテスト＆ドキュメント生成（CI と同じ手順）
  uv sync --frozen
  pytest tests/ --cov=src
  mkdocs build   # または sphinx-build -b html docs src/_build/html

  # AGENTS.md を最新化するだけで OK
  python scripts/gen_agents_md.py
  ```
このプロジェクトにより、コミットごとに一貫した品質保証・ドキュメント管理が自動化されるため、開発者は実装やバグ修正に専念できるようになります。<!-- MANUAL_START:architecture -->

<!-- MANUAL_END:architecture -->
```mermaid
graph TB
    %% Auto-generated architecture diagram

    subgraph agents_docs_sync [fa:fa-python agents-docs-sync]
        direction TB
        subgraph docgen [docgen]
            direction TB
            docgen_collectors["collectors"]:::moduleStyle
            subgraph docgen_utils [utils]
                direction TB
                docgen_utils_llm["llm"]:::moduleStyle
            end
            class docgen_utils moduleStyle
            subgraph docgen_cli [cli]
                direction TB
                docgen_cli_commands["commands"]:::moduleStyle
            end
            class docgen_cli moduleStyle
            docgen_models["models"]:::moduleStyle
            subgraph docgen_archgen [archgen]
                direction TB
                docgen_archgen_detectors["detectors"]:::moduleStyle
                docgen_archgen_generators["generators"]:::moduleStyle
            end
            class docgen_archgen moduleStyle
            docgen_benchmark["benchmark"]:::moduleStyle
            docgen_detectors["detectors"]:::moduleStyle
            subgraph docgen_generators [generators]
                direction TB
                docgen_generators_services["services"]:::moduleStyle
                docgen_generators_parsers["parsers"]:::moduleStyle
            end
            class docgen_generators moduleStyle
            subgraph docgen_rag [rag]
                direction TB
                docgen_rag_strategies["strategies"]:::moduleStyle
            end
            class docgen_rag moduleStyle
            docgen_config["config"]:::moduleStyle
        end
        class docgen moduleStyle
    end

    docgen_collectors --> docgen_models
    docgen_collectors --> docgen_utils
    docgen_utils --> docgen_models
    docgen_utils_llm --> docgen_models
    docgen_cli --> docgen_archgen
    docgen_cli --> docgen_generators
    docgen_cli --> docgen_rag
    docgen_cli --> docgen_utils
    docgen_cli_commands --> docgen_rag
    docgen_cli_commands --> docgen_utils
    docgen_archgen --> docgen_detectors
    docgen_archgen --> docgen_generators
    docgen_archgen --> docgen_models
    docgen_archgen --> docgen_utils
    docgen_archgen_detectors --> docgen_models
    docgen_archgen_generators --> docgen_models
    docgen_benchmark --> docgen_models
    docgen_benchmark --> docgen_utils
    docgen_detectors --> docgen_utils
    docgen_generators --> docgen_archgen
    docgen_generators --> docgen_collectors
    docgen_generators --> docgen_detectors
    docgen_generators --> docgen_models
    docgen_generators --> docgen_utils
    docgen_generators_parsers --> docgen_detectors
    docgen_generators_parsers --> docgen_models
    docgen_generators_parsers --> docgen_utils
    docgen_rag --> docgen_utils
    docgen_rag_strategies --> docgen_utils

    classDef pythonStyle fill:#3776ab,stroke:#ffd43b,stroke-width:2px,color:#fff
    classDef dockerStyle fill:#2496ed,stroke:#1d63ed,stroke-width:2px,color:#fff
    classDef dbStyle fill:#336791,stroke:#6b9cd6,stroke-width:2px,color:#fff
    classDef moduleStyle fill:#f9f9f9,stroke:#333,stroke-width:2px
```

## Services

### agents-docs-sync
- **Type**: python
- **Description**: コミットするごとにテスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン
- **Dependencies**: anthropic, hnswlib, httpx, jinja2, openai, outlines, pip-licenses, psutil, pydantic, pytest, pytest-cov, pytest-mock, pyyaml, ruff, sentence-transformers, torch

## 使用技術

- Python
- Shell

## 依存関係

- **Python**: `pyproject.toml` または `requirements.txt` を参照

## セットアップ


## 前提条件

- Python 3.12以上



## インストール


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

## ビルドおよびテスト
### ビルド

```bash
uv sync
uv build
uv run python3 docgen/docgen.py
```
### テスト

```bash
bash scripts/run_tests.sh
uv run pytest tests/ -v --tb=short
```
## コマンド

プロジェクトで利用可能なスクリプト:

| コマンド | 説明 |
| --- | --- |
| `agents_docs_sync` | docgen.docgen:main |

### `agents_docs_sync` のオプション

| オプション | 説明 |
| --- | --- |
| `--config` | 設定ファイルのパス |
| `--quiet` | 詳細メッセージを抑制 |
| `--detect-only` | 言語検出のみ実行 |
| `--no-api-doc` | APIドキュメントを生成しない |
| `--no-readme` | READMEを更新しない |
| `--build-index` | RAGインデックスをビルド |
| `--use-rag` | RAGを使用してドキュメント生成 |
| `--generate-arch` | アーキテクチャ図を生成（Mermaid形式） |

---

*このREADME.mdは自動生成されています。最終更新: 2025-12-12 15:27:28*