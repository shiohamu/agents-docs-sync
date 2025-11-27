# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、コミットごとに自動でテストを実行し、最新のドキュメントを生成して `AGENTS.md` を更新するパイプラインです。  
Python 3 とシェルスクリプトを組み合わせて構築され、以下のような特徴があります。

- **ビルドフロー** – `uv sync`, `uv build`, および `uv run python3 docgen/docgen.py` により依存関係の同期・パッケージ化とドキュメント生成を実行します。  
- **テスト環境** – Python 版は Pytest（+pytest‑cov, pytest‑mock）で、Node.js と Go のユニットテストも同時に走らせます (`npm test`, `go test ./...`)。  
- **ドキュメント生成** – YAML ベースの定義から API ドキュメントを自動的に作成し、その結果をプロジェクトルートの `AGENTS.md` に反映します。  
- **依存関係管理** – Python は `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` を使用し、これらは `uv.lock` で固定化されます。  
- **コーディング規約** – コード品質を保つために Ruff ライナーが導入されています（`ruff check . --fix` が推奨）。  

このセットアップにより、コードベースとドキュメントの整合性を手動で管理する負担を大幅に軽減し、一貫した品質保証プロセスを実現します。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 23:33:57*