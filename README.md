# agents-docs-sync

<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->
本プロジェクトは、リポジトリにコミットがあるたびに自動で以下のタスクを実行するパイプラインです。  
- **テスト実行**：Python（pytest）、JavaScript (npm test)、Go (`go test`) の各言語環境でユニット・統合テストを走らせます。  
- **ドキュメント生成**：`docgen/docgen.py` を用いて YAML 形式の設定情報から Markdown ドキュメント（AGENTS.md 等）を再構築します。  
- **自動更新**：最新のビルド成果物やテストレポートに基づき、AGENTS.md の内容が同期されます。

## 技術スタック
| 言語 | 主な用途 |
|------|----------|
| Python | テスト実行・docgen スクリプト（`pyyaml`, `pytest`, など） |
| Shell   | ビルドスクリプトや CI/CD のエントリポイント |
| JavaScript (npm) | フロントエンド関連テスト |
| Go      | バックエンドユニットテスト |

## 主要依存関係
- `pyyaml>=6.0.3` : YAML パーサ／生成  
- `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` : Python テスティングフレームワーク  

## ビルド手順
```bash
# 依存関係の同期・ビルド
uv sync          # uv を使用したパッケージインストールとロックファイル生成
uv build         # プロジェクトをビルド（必要に応じてバイナリやアーカイブ作成）
uv run python3 docgen/docgen.py  # ドキュメントの再生成
```

## テスト実行コマンド
```bash
# Python のテスト
uv run pytest tests/ -v --tb=short

# JavaScript / TypeScript のテスト (npm がインストールされている前提)
npm test

# Go のユニットテスト（全パッケージ）
go test ./...
```

## コーディング規約
- **リンター**: `ruff` を用いてコード品質を統一。  
  ```bash
  uv run ruff check .          # 静的解析とフォーマットチェック
  uv run ruff format .         # 自動整形（必要に応じて）
  ```

## ワークフロー概要

1. **コミット** → GitHub Actions / CI がトリガー  
2. 上記ビルド・テストスクリプトが順次実行  
3. `docgen.py` により最新の設定情報から Markdown ドキュメントを生成し、AGENTS.md を更新  
4. すべて完了したら成果物（レポートやバイナリ）がアーティファクトとして保存

これにより、コードベースとドキュメントが常に同期される自動化パイプラインが構築されています。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-26 13:29:38*