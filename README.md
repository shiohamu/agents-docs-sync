# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、コードベースに対するコミットごとに自動でテストを実行し、ドキュメント生成スクリプト `docgen/docgen.py` を走らせて **AGENTS.md** ファイルを最新状態へ更新します。
このプロジェクトは Python とシェルベースのツールチェーンで構成され、CI/CD 環境やローカル開発時に同一パイプラインを再現できるよう設計されています。

### 主な機能
- **自動テスト実行**：`pytest`, `npm test`, および Go のユニットテスト（`go test ./...`）が順次走ります。
- **ドキュメント生成**：Python スクリプト `docgen/docgen.py` がプロジェクト内のコードや設定から最新の Markdown ドキュメントを作成します。
- **AGENTS.md の更新**：テストとドキュメント生成が成功した後、自動で AGENTS.md を書き換えます。これにより外部への公開情報が常に同期されます。

### 環境構築
```bash
# 依存ツールのインストール（uv が必要）
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクトディレクトリへ移動し、Python の環境を同期・ビルド
uv sync          # 依存パッケージ (pyyaml, pytest 等) を取得
uv build         # 必要に応じて C 拡張などのビルド

# ドキュメント生成スクリプト実行（手動で確認したい場合）
uv run python3 docgen/docgen.py
```

### テストと CI パイプライン
```bash
# Python のテスト
uv run pytest tests/ -v --tb=short

# Node.js プロジェクトのテスト (もし併設されているなら)
npm test

# Go モジュール内の全パッケージを対象にしたテスト
go test ./...
```

### コーディング規約とリンタ
- Python のコードは `ruff` でスタイルチェック・フォーマットが行われます。
```bash
uv run ruff check . --fix   # 静的解析と自動修正を実施
```
- シェルスクリプトやその他言語についても同様に linting を導入している場合は、プロジェクト内の `.gitlab-ci.yml` や `Makefile` で呼び出すようになっています。

### 開発フロー
1. **ブランチ作成**：新機能やバグ修正を行う際に feature/ ブランチを切ります。
2. **ローカルテスト実行**：上記の `uv run pytest` 等で必ず成功させてからコミットします。
3. **プッシュ & PR 作成**：GitHub/GitLab の CI が自動的にトリガーされ、パイプラインが走ります。
4. **AGENTS.md 更新確認**：CI 成功後、`docs/AGENTS.md` を GitHub 上でチェックし差分をレビューします。

### まとめ
- Python とシェルの組み合わせにより、複数言語プロジェクトでも一貫したビルド・テストフローが実現。
- `uv` の高速依存解決と環境管理でローカル開発もスムーズ。
- ドキュメント生成からファイル更新まで自動化することで、手作業によるミスを排除し、常に最新の情報が公開されます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 14:13:28*
