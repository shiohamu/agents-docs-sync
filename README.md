# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
`agents-docs-sync` は、リポジトリへのコミットごとに以下の３つを自動で実行する CLI パイプラインです。  
- **テスト**：pytest などのユニット／インテグレーションテストを実行し、ビルド失敗時はすぐ通知します。  
- **ドキュメント生成**：`docgen/` 内にある Python コードから API ドキュメント（Sphinx / MkDocs 用）と `AGENTS.md` を自動作成します。コードコメントや型ヒントを解析し、最新の仕様書が常に反映されます。  
- **AGENTS.md の更新**：`docgen/models/agents.py` に定義された `AgentsConfig` クラスからエージェント構成情報（名前・説明・パラメータ）を抽出し、Markdown 形式でまとめ直します。

---

### アーキテクチャ

```
┌───────────────────────┐
│ git commit / CI trigger │
├─────────────▲───────────┤
│             │           │
│    agents-docs-sync CLI (Python) ──> ① run_tests()
│                                   │          ↓
│                                   │   pytest/flake8 等
│                                   │          ↑
│                                   │
│                       ② generate_docs() → Sphinx/MkDocs build
│                                   │          ↓
│                         docgen/docgen.py (Jinja2 templates)
│                                   │
├─────────────▼──────────────────┤
│   ③ update_AGENTS.md           │
│        ← parse_agents_config() │
│            from AgentsConfig    │
└───────────────────────▲───────┘
                     │
               (git add & commit)
```

- **CLI**：`typer` を使用し、`agents-docs-sync --help` でヘルプが表示されます。  
- **Python スクリプト**（`docgen.docgen:main`）：テスト実行は `subprocess.run()` によりシェルコマンドを呼び出し、ドキュメント生成は Jinja2 テンプレートと型情報から Markdown を作成します。  
- **エントリポイント**：pyproject.toml で `"agents-docs-sync"` と `"agents_docs_sync"` が `docgen.docgen:main` にマッピングされており、pip install 後はどちらの名前でも実行可能です。

---

### 主な機能

| 機能 | 内容 |
|------|------|
| **自動テスト** | コミット時に全テストを走らせ、失敗した場合はビルドステータスで即座に通知。CI との連携が容易です。 |
| **API ドキュメント生成** | `docgen/models` 内の型定義と docstring を元に Sphinx の `.rst` ファイルを自動作成し、静的サイトへビルドします。 |
| **AGENTS.md 自動更新** | エージェント構成（クラス名・説明・パラメータ）を `AgentsConfig` から抽出して Markdown 表に変換。手入力のミスや古い情報が残るリスクを排除。 |
| **CLI オプション** | `--skip-tests`, `--dry-run`, `-v/--verbose` 等で実行内容を細かく制御可能です。また、環境変数でデバッグログレベル調整もサポートします。 |
| **拡張性** | テンプレートは Jinja2 で記述されているため、新しいドキュメント形式や出力先（GitHub Pages, ReadTheDocs 等）へ簡単に移植できます。 |

---

### 使用例

```bash
# インストール後、リポジトリルートから実行
$ agents-docs-sync          # すべての処理を走らせる
$ agents-docs-sync --skip-tests   # テストはスキップしてドキュメントだけ生成する

# ヘルプ確認
$ agents-docs-sync --help
```

コミット時に自動で実行したい場合は、CI のジョブや Git フック（pre‑commit）に `agents-docs-sync` を組み込むと一連のドキュメント管理が完結します。  

---

### まとめ

- **コード品質**：テスト失敗時に即通知し、不具合を早期発見。  
- **ドキュメント整備**：手動更新不要で常に最新情報を保持。  
- **開発フロー統合**：Python/シェルベースの軽量ツールが、既存 CI/CD パイプラインへ簡単組み込み可能。  

`agents-docs-sync` を導入すれば、リポジトリ内でエージェント関連ドキュメントを自動同期しつつ、高い品質と整合性を維持できます。





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

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 06:21:41*