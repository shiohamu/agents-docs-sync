# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
Python とシェルで構築された CLI ツール **agents‑docs‑sync** は、複数のリポジトリに散在するエージェント関連ドキュメントを一元管理・同期させるためのユーティリティです。  
主な機能と技術的設計は以下の通りです。

- **CLI エントリポイント**  
  - `agents-docs-sync` / `agents_docs_sync`: pyproject.toml の `[project.scripts]` に定義され、実行時に `docgen.docgen:main` を呼び出します。  
  - ヘルプ表示は `--help` オプションで確認でき（例：`agents-docs-sync --help`）、コマンドライン引数を通じて同期対象やオプション設定が指定可能です。

- **構成モデル** (`AgentsConfig`)  
  - `docgen/models/agents.py` に実装され、JSON/YAML 等で読み込むことによりリポジトリ URL、ブランチ名、ドキュメントパスなどを管理します。  
  - このクラスはデータ検証（pydantic ベース）と既定値設定が行われており、CLI の `--config` オプションで読み込むことができます。

- **アーキテクチャ**  
  ```
  ├─ docgen/
  │   ├─ __init__.py
  │   ├─ models/agents.py      ← AgentsConfig 定義
  │   └─ docgen.py             ← main() が CLI を解析し、同期ロジックを実行
  ├─ scripts/                 ← 必要に応じてシェルスクリプトでラップ
  └─ pyproject.toml           ← ビルド・依存関係定義（scripts セクション含む）
  ```
  - `main()` は argparse を用いてオプション解析 → 設定読み込み → ドキュメント生成/同期処理を順次実行します。  
  - 実際の同期ロジックは GitPython 等でリポジトリクローン／更新し、対象ファイル（Markdown, YAML）を取得・比較して差分があれば書き込みます。

- **主要モジュールと機能**  
  | モジュール | 主な役割 |
  |------------|----------|
  | `docgen.docgen` | CLI エントリポイント、引数解析、同期処理のコーディネータ |
  | `docgen.models.agents.AgentsConfig` | 設定ファイル（JSON/YAML）をパースし検証するデータモデル |
  | シェルスクリプト (`scripts/`) | CI/CD パイプラインやローカル開発環境での簡易呼び出し用ラッパー |

- **使用例**  
  ```bash
  # 設定ファイルを指定して同期実行
  agents-docs-sync --config path/to/config.yaml

  # ヘルプ表示
  agents-docs-sync --help
  ```

- **開発・ビルド手順（pyproject.toml）**  
  ```toml
  [build-system]
  requires = ["setuptools>=42", "wheel"]
  build-backend = "setuptools.build_meta"

  [tool.setuptools.packages.find]
  where = ["src"]

  [project.scripts]
  agents-docs-sync = "docgen.docgen:main"
  agents_docs_sync = "docgen.docgen:main"
  ```

- **拡張性**  
  - 設定モデルを継承して新しいドキュメントタイプ（API Docs, README 等）に対応可能。  
  - シェルスクリプトで GitHub Actions と連携し、PR 作成時の自動同期も容易。

この構造により **agents‑docs‑sync** は軽量かつ再利用性が高く、多数のエージェントプロジェクト間でドキュメント整合性を保ちやすいツールとなっています。





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
```
```bash
uv build
```
```bash
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest tests/ -v --tb=short
```
```bash
npm test
```
```bash
go test ./...
```





---

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 11:20:48*