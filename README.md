# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要


`agents-docs-sync` は、Python と Shell スクリプトで構成された CI ユーティリティです。GitHub にコードが push されるたびに自動的に実行され、以下の３つを同時進行で完了します。

1. **テストと品質検証**  
   - `pytest` と `coverage.py` を組み合わせて単体・統合テストを走らせます。失敗した場合はビルドが中断し、GitHub Actions のログに詳細なエラー情報が出力されます。  
   - カバレッジ報告（`.xml`, `.html`）はアーティファクトとして保存できるため PR で即座に確認できます。

2. **最新の API/ユーザーガイド生成**  
   - Sphinx と `sphinx-autodoc` を使用して、Python モジュールから自動的にドキュメントをビルド。静的 HTML は GitHub Pages にデプロイ可能な形式で出力されます。

3. **AGENTS.md の自動同期**  
   - リポジトリ内のエージェント（Python モジュール）を走査し、モジュール名と簡易説明を抽出。  
   - 抽出した情報で `AGENTS.md` を上書き保存後、自動コミット＆push して最新状態に保ちます。

このワークフローは `.github/workflows/ci.yml` に定義されており、**push 一回でテスト・ドキュメント生成・AGENTS.md 更新がすべて実施**。  
> **メリットまとめ**  
> - コード変更とドキュメント・リスト更新を同時に行えるため、人為的ミスの削減。  
> - テスト失敗やカバレッジ低下を即座に検知し、品質保証が徹底できる。  
> - AGENTS.md の手動編集不要で、エージェント追加・変更が自動反映。

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

*このREADMEは自動生成されています。最終更新: 2025-11-21 16:08:23*
