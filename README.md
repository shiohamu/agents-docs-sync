# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要
<!-- MANUAL_START:description -->
`agents-docs-sync` は、Python・JavaScript/TypeScript・C の 3 種類の言語で書かれたコードベースに対して **自動化された CI/CD パイプライン** を提供します。GitHub に push が入ると GitHub Actions がトリガーされ、以下のフローが実行されます。

1. **ビルド・テスト**
   - Python → `pytest`
   - JavaScript/TypeScript → `jest` / `ts-jest`
   - C → `make test`

   これらは並列に走り、いずれかの失敗でビルドを停止します。品質保証と継続的インテグレーションが同時に実現されます。

2. **API ドキュメント生成**
   - Python → Sphinx（reStructuredText）
   - JavaScript/TypeScript → JSDoc + TypeDoc
   - C → Doxygen

   それぞれのツールで API の詳細を抽出し、`docs/` ディレクトリに統合。各言語ごとのベストプラクティスに沿ったドキュメントが自動的に作成されます。

3. **AGENTS.md 自動更新**
   - 生成されたドキュメントから関数・クラスのメタ情報（名前、説明、引数、戻り値）を抽出し、差分置換で `AGENTS.md` を再構築。手作業による修正が不要になり、一貫性と即時反映が保証されます。

4. **成果物公開**
   - 成功したビルドは GitHub Pages（または `gh-pages` ブランチ）へデプロイされ、外部から閲覧可能。CI の結果も可視化しつつ、最新の API ドキュメントとエージェント一覧が常に公開状態です。

このパイプラインを利用することで、多言語リポジトリでも **品質保証** と **ドキュメント整備** を同時かつ自動で実行できるため、開発者体験（DX）とプロジェクトの保守性が大幅に向上します。
<!-- MANUAL_END:description -->
<!-- MANUAL_START:description -->

## 概要
<!-- MANUAL_START:description -->
`agents-docs-sync` は、Python・JavaScript/TypeScript・C の 3 種類の言語で書かれたコードベースに対して **自動化された CI/CD パイプライン** を提供します。GitHub に push が入ると GitHub Actions がトリガーされ、以下のフローが実行されます。

1. **ビルド・テスト**
   - Python → `pytest`
   - JavaScript/TypeScript → `jest` / `ts-jest`
   - C → `make test`

   これらは並列に走り、いずれかの失敗でビルドを停止します。品質保証と継続的インテグレーションが同時に実現されます。

2. **API ドキュメント生成**
   - Python → Sphinx（reStructuredText）
   - JavaScript/TypeScript → JSDoc + TypeDoc
   - C → Doxygen

   それぞれのツールで API の詳細を抽出し、`docs/` ディレクトリに統合。各言語ごとのベストプラクティスに沿ったドキュメントが自動的に作成されます。

3. **AGENTS.md 自動更新**
   - 生成されたドキュメントから関数・クラスのメタ情報（名前、説明、引数、戻り値）を抽出し、差分置換で `AGENTS.md` を再構築。手作業による修正が不要になり、一貫性と即時反映が保証されます。

4. **成果物公開**
   - 成功したビルドは GitHub Pages（または `gh-pages` ブランチ）へデプロイされ、外部から閲覧可能。CI の結果も可視化しつつ、最新の API ドキュメントとエージェント一覧が常に公開状態です。

このパイプラインを利用することで、多言語リポジトリでも **品質保証** と **ドキュメント整備** を同時かつ自動で実行できるため、開発者体験（DX）とプロジェクトの保守性が大幅に向上します。
<!-- MANUAL_END:description -->

<!-- MANUAL_END:description -->

## 使用技術

- Python
- JavaScript
- C

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.8以上
- Node.js (推奨バージョン: 18以上)

### インストール

```bash
uv sync
```

```bash
npm install
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

*このREADMEは自動生成されています。最終更新: 2025-11-21 12:15:28*
