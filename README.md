# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
Python とシェルスクリプトで構築された **agents-docs-sync** は、エージェント定義のドキュメントを自動生成・同期するための CLI ツールです。  
ツールは `pyproject.toml` の `[project.scripts]` により `agents-docs-sync` コマンドとして公開されており、内部では **docgen.docgen:main** を実行します。

### 技術スタックとアーキテクチャ
- **Python 3.11+**：メインロジックを記述。  
- **Pydantic v2**（`docgen/models/agents.py`）：設定ファイルのスキーマ定義 (`ProjectOverview`, `AgentsConfigSection`, `AgentsGenerationConfig`, `AgentsDocument`) を通じて、YAML/YML 形式で提供される構成を検証。  
- **Jinja2**（内部テンプレートエンジン）：AGENTS.md のマークダウン出力に使用し、柔軟なレイアウトが可能。  
- **GitHub Actions / CI/CD パイプライン** で簡単に組み込めるよう設計されており、リポジトリクローンから `agents-docs-sync --help` のヘルプ表示まで一連のコマンドをサポート。  
- **シェルスクリプト**：Windows でも Bash が利用できない環境向けに簡易ラッパーが用意され、CLI 実行時のエイリアスやオーバーロード機能を提供。

### 主な機能
| 機能 | 説明 |
|------|-----|
| **構成ファイル駆動** | `agents.yaml` でプロジェクト概要・各エージェント設定（入力/出力型、説明文）を宣言。Pydantic が検証し、不正な定義は即座に報告。 |
| **AGENTS.md 自動生成** | 設定ファイルから構造化データ (`AgentsDocument`) を作成し、Jinja2 テンプレートで整形されたマークダウンを出力。既存のドキュメントと差分検知して更新箇所のみを書き換え。 |
| **同期機能** | 生成した `AGENTS.md` とリポジトリ内の `docs/agents/` フォルダーにある個別エージェントファイルを自動で一致させ、重複や欠落がないよう監査。 |
| **CLI オプション** | `--dry-run`, `--verbose`, `--config <path>` などの便利なフラグを備え、開発者は変更前に確認できる。また `agents-docs-sync --help` によって全オプションが表示されます。 |
| **CI/CD 向けスクリプト** | GitHub Actions 用サンプルワークフロー（`.github/workflows/docs.yml`）を同梱し、PR での自動ドキュメント更新やビルド時に統合テストが可能です。 |

### ワークフローレイアウト
1. **リポジトリクローン**  
   ```bash
   git clone https://github.com/your-org/agents-docs-sync.git
   cd agents-docs-sync
   ```
2. **設定ファイル作成／更新** (`agents.yaml`) → `ProjectOverview` でプロジェクト全体のメタ情報を記述。  
3. **ドキュメント生成**  
   ```bash
   agents-docs-sync --config agents.yaml
   ```
4. **差分確認・コミット**（CI/CD が自動実行）  

### 拡張性と保守性
- 新しいエージェントタイプやカスタムフィールドを追加する場合は、`docgen/models/agents.py` の Pydantic クラスに属性を追記し、Jinja2 テンプレート側で `{{ agent.<field> }}` を参照すれば完結。  
- 既存の構成モデル (`AgentsConfigSection`, `AgentsGenerationConfig`) は再利用可能なデータクラスとして設計されているため、他プロジェクトへの移植も容易です。

### 開発者向けリソース
| リソース | 内容 |
|----------|------|
| **ドキュメント** (`docs/api.md`, `CONFIG_GUIDE.md`) | API 仕様・設定項目詳細を網羅。 |
| **Release ノート** (`RELEASE.md` の動作確認セクション) | 各リリースでの変更点とテスト手順が記載。 |
| **サンプル構成ファイル** | `docs/agents.yaml.sample` を参照し、即座に試せる設定例を提供。 |

このような設計によって、エージェントドキュメント作業の煩雑さを大幅に削減し、CI/CD で自動化された高品質ドキュメント生成パイプラインを実現しています。





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

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 19:10:31*