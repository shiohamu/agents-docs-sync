# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要

`agents-docs-sync` は、GitHub に push された変更をトリガーにして実行される CI/CD パイプラインです。主な機能は以下の通りです。

| フロー | 実施内容 |
|--------|----------|
| **テスト** | Python のユニット／統合テスト（`pytest`）を自動で走らせ、コード品質とバグ検出を行います。 |
| **ドキュメント生成** | Sphinx などのツールを使ってソースコードから API ドキュメントやユーザー向けガイドをビルドします。|
| **AGENTS.md の更新** | リポジトリ内にあるエージェント実装（Python モジュール）情報を自動で収集し、`AGENTS.md` に最新の一覧と簡易説明を書き込みます。 |

### 技術スタック
- **言語**: Python (テスト・ドキュメント生成)、Shell (ビルドスクリプトやファイル操作)
- **CI ツール**: GitHub Actions（ワークフロー定義は `.github/workflows` 配下）
- **その他依存ライブラリ**:
  - `pytest`, `coverage`
  - Sphinx, sphinx-autodoc
  - 任意のスクリプト用ユーティリティ (`jq`, `sed` 等)

### 主なメリット

1. **自動化で手間削減**  
   コードを書いたらすぐにテストとドキュメントが更新され、レビュー時に最新情報を確認できます。

2. **一貫性のあるドキュメント品質**  
   生成スクリプトは同じテンプレート・設定で実行するため、バージョン間やプロジェクト内で文書スタイルが統一されます。

3. **エージェント情報を常に最新状態へ保つ**  
   `AGENTS.md` は手動更新の必要がなくなり、新しいエージェント追加・削除時にも即座に反映します。

### 使い方

1. リポジトリをクローンし、Python 環境（仮想環境推奨）で依存パッケージをインストール。  
   ```bash
   pip install -r requirements.txt
   ```

2. GitHub Actions が設定されているため、ローカルの `git push` だけで自動テスト・ドキュメント生成が走ります。

3. 必要に応じて `.github/workflows/ci.yml` のスクリプトを調整し、新しいツールやステップを追加できます。  

---  
このプロジェクトは、Python ベースのエージェント開発チームが継続的インテグレーションとドキュメント管理を簡単に行えるよう設計されています。

<!-- MANUAL_END:description -->

## 使用技術

- Python
- Shell

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.8以上

### インストール

```bash
uv sync
```

<!-- MANUAL_END:setup -->

## ビルドおよびテスト

### ビルド

```bash
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest
uv run python3 -m pytest test
uv run pytest tests/ -v --tb=short
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-21 14:50:14*
