# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
- **プロダクト名**：agents‑docs‑sync  
  - コミットごとに自動でテスト実行、ドキュメント生成（Sphinx/MkDocs 等）、`AGENTS.md` の更新を行う CI/CD パイプライン。  

- **主な構成**  
  | 層 | 技術・ツール | 主な役割 |
  |----|--------------|----------|
  | CLI & コアロジック | Python (`docgen.docgen:main`) | `agents-docs-sync` スクリプトのエントリポイント。テスト実行、ドキュメント生成、ファイル差分取得・マージを制御 |
  | オーケストレーション | Bash/シェルスクリプト | Git フック（pre‑commit / post‑merge）や CI スクリプトで呼び出し。環境変数とロギングを統一化 |
  | テストフレームワーク | PyTest + coverage | コード品質維持のために自動実行、テスト結果は GitHub Actions へ報告 |
  | ドキュメント生成 | Sphinx / MkDocs（設定ファイル `conf.py`）| ソースコードとドキュメンテーションを統合し HTML/Markdown をビルド。CI 上で自動更新 |
  | バージョニング & デプロイ | Poetry + pyproject.toml | プロジェクト管理、依存関係解決、バージョンタグ付与（`agents-docs-sync --help` によるヘルプ表示） |

- **主要機能**  
  - **自動テスト実行**：コミット時に PyTest を走らせ、失敗した場合はビルドを停止。CI パイプラインでカバレッジの閾値もチェック。
  - **文書生成と差分管理**：`docgen.docgen:main` が Sphinx/MkDocs の `build-docs.sh` を呼び、最新の API ドキュメントをビルド。変更があれば Git にコミットし、`AGENTS.md` を更新。
  - **自動化された AGENTS.md 更新**：エージェント定義ファイル（例: YAML/JSON）からメタデータ抽出し `AGENTS.md` の表を再生成。差分があれば PR に添付。
  - **CLI ユーティリティ**：  
    ```bash
    agents-docs-sync --help
    ```
    オプションでテストのみ、ドキュメントのみ、または両方の実行モードを選択可能。  
- **アーキテクチャ的強み**  
  - Python を中心に書かれたビジネスロジックとシェルベースのオーケストレーションで高速な CI 実装が可能。
  - Poetry による依存管理は reproducible な環境を保証し、`pyproject.toml` の `scripts` セクションにより直接 CLI を公開している点も利便性向上。
  - テストとドキュメント生成のパイプラインが一元化されており、コードベース変更時の品質保証を継続的に確保。

- **改善提案**  
  - コードレビューで指摘された高優先度クオリティ問題（PEP8 遵守・型ヒント整備）を即対応。
  - CI にコード品質ゲート（`flake8`, `mypy`) を追加し、プルリクエスト時に自動チェック。
  - 定期的なセキュリティ監査とパフォーマンスベンチマークの導入で長期安定性を確保。





## 使用技術

- Shell
- Python

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-29 06:12:18*