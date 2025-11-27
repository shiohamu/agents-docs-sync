# agents-docs-sync

<!-- MANUAL_START:description -->
> **IMPORTANT!!**
>
> まだドキュメント出力が安定していないため、内容については正確性に欠けます。プルリクエスト待ってます。
<!-- MANUAL_END:description -->
agents-docs-sync は、コミットごとに自動でテストを実行し、ドキュメント生成スクリプトを走らせて `AGENTS.md` を最新化する CI/CD パイプラインです。  
プロジェクトは Python とシェルスクリプトの両方で構成されており、次のような機能とフローがあります。

- **自動テスト** – Pytest（Python）、npm テスト（JavaScript/TypeScript）、Go のユニットテストを同時に実行します。  
- **ドキュメント生成** – `docgen/docgen.py` を走らせて API ドキュメントとマークダウンファイルを作成し、GitHub 上の `AGENTS.md` に反映させます。  
- **CI のトリガー** – Git へのプッシュまたは PR が行われるたびに上記全工程が実行され、常に最新状態を保ちます。

### 使用言語・ツール
| 言語 | 主なライブラリ / ツール |
|------|------------------------|
| Python | `pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1` |
| Shell | 標準シェルスクリプト（ビルド・テスト実行用） |

### 依存関係
- **Python**  
  - `pyyaml >= 6.0.3`
  - `pytest >= 7.4.0`
  - `pytest-cov >= 4.1.0`
  - `pytest-mock >= 3.11.1`

### ビルドフロー
```bash
# 環境構築とパッケージ同期
uv sync

# パッケージビルド（必要に応じて）
uv build

# ドキュメント生成スクリプト実行
uv run python3 docgen/docgen.py
```

### テストフロー
```bash
# Python のユニットテスト
uv run pytest tests/ -v --tb=short

# npm（JavaScript/TypeScript）テスト
npm test

# Go 言語のパッケージ単位で実行
go test ./...
```

### コーディング規約
- **リンター**: `ruff` を使用してコード品質を保ちます。  
  実行例：`uv run ruff check . --fix`

この構成により、開発者はコミットごとに自動テスト・ドキュメント更新が保証されるため、継続的インテグレーション環境で高い品質を維持できます。

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

*このREADME.mdは自動生成されています。最終更新: 2025-11-27 13:21:11*