# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要

**agents-docs-sync** は、Python と Shell スクリプトを組み合わせた CI パイプラインです。  
リポジトリへの **push 1 回で以下の処理が自動実行されます**

| フェーズ | 実施内容 |
|---------|----------|
| テスト & 品質検証 | `pytest` と `coverage.py` を併用し、単体・統合テストを走らせます。失敗した場合はビルドが中断され、GitHub Actions のログに詳細なエラー情報とカバレッジ報告（`.xml`, `.html`）が残ります。 |
| ドキュメント生成 | Sphinx + `sphinx-autodoc` で Python モジュールから API ドキュメントをビルドし、静的 HTML を `docs/` ディレクトリへ出力します（GitHub Pages 等へのデプロイが可能）。 |
| AGENTS.md 自動同期 | リポジトリ内のエージェントモジュールを走査して名前と簡易説明を抽出し、取得した情報で `AGENTS.md` を再生成。ファイル更新後は自動コミット＆push されるため、人手による編集作業が不要です。 |

### 主なメリット
- **コード変更に即座にドキュメント・リストを同期**：開発者は一度の push でテスト、文書化、およびエージェント一覧更新まで完了でき、人為ミスを最小限に抑えます。  
- **品質保証が継続的に反映**：カバレッジ低下やテスト失敗はすぐに検知され、CI のログで詳細確認できます。  
- **保守性の高い実装**：Python スクリプトと軽量な Shell ラッパーだけで構成し、導入・メンテナンスが容易です。

### 技術スタック
- **言語**: Python, Bash/Shell  
- **CI ツール**: GitHub Actions (`.github/workflows/ci.yml`)  
- **テストフレームワーク**: pytest + coverage.py  
- **ドキュメント生成**: Sphinx (autodoc)  

このパイプラインを導入することで、コードベースとその周辺情報の一貫性が保たれ、開発サイクル全体で品質向上に寄与します。

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

*このREADMEは自動生成されています。最終更新: 2025-11-22 18:13:16*
