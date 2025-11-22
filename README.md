# agents-docs-sync

<!-- MANUAL_START:description -->
## 概要

**agents-docs-sync** は、Python と Shell スクリプトを組み合わせた GitHub Actions ベースの CI パイプラインです。
リポジトリへの **push 1 回で以下の処理が自動実行されます**

| フェーズ | 実施内容 |
|---------|----------|
| **テスト & 品質検証** | `pytest` と `coverage.py` を併用し、単体・統合テストを走らせるとともにカバレッジ報告（`.xml`, `.html`）を生成。失敗した場合はビルドが中断され、GitHub Actions のログで詳細なエラー情報と共に通知されます。また `--maxfail=1` などのオプションで早期停止も可能です。 |
| **ドキュメント生成** | `README.md` と `docs/api.md` が出力されます
| **AGENTS.md 自動同期** | リポジトリ内のエージェントモジュール (`agents/*.py`) を走査し、クラス名と docstring の冒頭行を抽出して `AGENTS.md` を再生成します。このファイルは GitHub Actions で自動コミット＆pushされるため、人手による編集作業が不要です。 |

### 主なメリット

- **変更即時反映**：開発者は一度の push だけでテスト、ドキュメント生成、およびエージェント一覧更新まで完了でき、ミスを最小限に抑えられます。
- **継続的品質保証**：カバレッジ低下やテスト失敗はすぐに検知され、CI のログで詳細確認が可能です。必要に応じて `coverage` スコア閾値を設定し、ビルド停止させることもできます。
- **保守性の高い実装**：Python スクリプトと軽量な Shell ラッパーだけで構成されており、新しいエージェントやテストケースが追加された際にも最小限の変更で済みます。

### 技術スタック

- **言語**: Python, Bash/Shell
- **CI ツール**: GitHub Actions (`.github/workflows/ci.yml`)
- **テストフレームワーク**: pytest + coverage.py

このパイプラインを導入することで、コードベースとその周辺情報の一貫性が保たれ、開発サイクル全体で品質向上に寄与します。

### 使用方法

```bash
user@hogehoge: ~$ agents_docs_sync --help

usage: agents_docs_sync [-h] [--version] [--config CONFIG] [--detect-only] [--no-api-doc] [--no-readme] {commit-msg,hooks} ...

汎用ドキュメント自動生成システム

positional arguments:
  {commit-msg,hooks}  実行するコマンド
    commit-msg        コミットメッセージ生成
    hooks             Git hooksの管理

options:
  -h, --help          show this help message and exit
  --version           show program's version number and exit
  --config CONFIG     設定ファイルのパス
  --detect-only       言語検出のみ実行
  --no-api-doc        APIドキュメントを生成しない
  --no-readme         READMEを更新しない
```
<!-- MANUAL_END:description -->

## 使用技術

- Python
- Shell

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.8以上

### インストール

・GitHub
```bash
git clone https://github.com/shiohamu/agents-docs-sync.git
uv sync
```

・pip
```bash
pip install agents_docs_sync
```

・uv
```bash
uv add agents_docs_sync
```

など
<!-- MANUAL_END:setup -->

## ビルドおよびテスト

### ビルド

```bash
uv run python3 docgen/docgen.py
```

### テスト

```bash
uv run pytest
npm test
uv run pytest tests/ -v --tb=short
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-22 19:01:16*
