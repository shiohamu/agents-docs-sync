# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、ソースコードのコミットごとに自動でテストを実行し、ドキュメントを生成して `AGENTS.md` を更新する CI/CD パイプラインです。  
Python とシェルスクリプトだけで構成されており、依存関係は `uv` で管理します。主な機能は次のとおりです。

- **テスト実行**：`pytest`, `npm test`, および Go のユニットテストを同時に走らせます。
- **ドキュメント生成**：Python スクリプト (`docgen/docgen.py`) が YAML で記述されたエージェント定義から Markdown を自動作成し、`AGENTS.md` に反映します。  
- **ビルドプロセス**：`uv sync`, `uv build`, および `uv run python3 docgen/docgen.py` の順に実行して環境を整えます。
- **コーディング規約**：全ての Python コードは `ruff` で linting が施され、コード品質が保証されています。

このプロジェクトにより、ドキュメントとテスト結果を常に最新状態に保ちつつ、手動更新によるヒューマンエラーを排除できます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 13:40:54*