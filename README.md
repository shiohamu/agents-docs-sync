# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
プロジェクトは、コミットごとに自動でテスト実行・ドキュメント生成をトリガーし、`AGENTS.md` を最新状態へ更新するCI/CDパイプラインです。  
主な構成要素

- **言語**: Python（メインロジック）＋シェルスクリプト（ビルド・テストワークフロー）
- **依存関係**:
  - `pyyaml>=6.0.3` – YAML ファイルをパースしてエージェント定義を読み込み
  - `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` – テスト実行とカバレッジ計測
- **ビルドフロー**:
  ```bash
  uv sync                # 依存関係をインストール・同期
  uv build               # パッケージング（必要に応じて）
  uv run python3 docgen/docgen.py   # ドキュメント生成スクリプト実行
  ```
- **テストフロー**:
  ```bash
  uv run pytest tests/ -v --tb=short    # Python テスト
  npm test                               # JavaScript／TypeScript のユニットテスト（必要に応じて）
  go test ./...                          # Go 言語のパッケージ単位で実行
  ```
- **コード品質**:
  - `ruff` を使用した静的解析とフォーマッティングを自動化し、コーディング規約違反を防止

### ワークフロー概要

1. コミットがプッシュされるたびに GitHub Actions が起動  
2. **ビルドステップ**で `uv sync` と `uv build` を実行 → 依存関係の解決とパッケージング
3. **テストステップ**で Python/JS/Go のユニットテストを並列に走らせ、失敗時はビルド停止  
4. テスト成功後 `docgen/docgen.py` を実行し、最新のエージェント定義から `AGENTS.md` を再生成  
5. 変更があれば自動でコミット／プッシュ（または PR 作成）される

### ドキュメント生成詳細

- エージェント情報は YAML ファイルに保持。Python スクリプトがこれを読み込み Markdown テンプレートへ埋め込む  
- 変更検知ロジック：`git diff --name-only HEAD~1 | grep 'agents/'` により、エージェント関連ファイルの更新のみ再生成
- `AGENTS.md` はプロジェクトルートに配置され、README 内や Wiki へのリンクで参照

### 実装ヒント

| タスク | 推奨コマンド |
|--------|--------------|
| 開発環境セットアップ | `uv sync --dev`（開発依存も同時インストール） |
| Lint & フォーマット | `ruff check . && ruff format .` |
| ドキュメント確認 | `cat AGENTS.md | head -n 20` |

この構成により、エージェントの追加・変更がコミットされるたびに自動的にドキュメントが更新され、一貫した情報提供を保証します。

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
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```



---

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 13:57:00*