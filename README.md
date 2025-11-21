# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要


**agents-docs-sync** は、Python と Shell を組み合わせた CI パイプラインです。
コミットが行われる度に以下の処理を自動で実施し、コードベースとドキュメントを常に同期させます。

1. **テスト実行** – `pytest` などでユニット・統合テストを走らせ、不具合を即座に検知します。
2. **ドキュメント生成** – ソースコードから API ドキュメント（Sphinx / pdoc 等）をビルドし、最新の `docs/` ディレクトリへ出力します。
3. **AGENTS.md の自動更新** – エージェント定義ファイルやコメントからメタ情報を抽出し、プロジェクト内にある `AGENTS.md` を再生成・コミットします。

これらのステップはすべて Python スクリプトとシンプルな Shell ラッパーで構成されるため、導入も保守もしやすい設計です。
CI ツール（GitHub Actions 等）との統合により、開発フローを中断することなく継続的デリバリーが実現できます。

---
**主な利点**

- コードとドキュメントの乖離を防止し、一貫した情報提供を保証。
- 手動で行っていた AGENTS.md 更新作業を自動化、人的ミス削減。
- CI パイプラインに組み込むことで品質担保が即時に反映される。

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
uv run python3 -m pytest test
uv run pytest tests/ -v --tb=short
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-21 17:01:59*
