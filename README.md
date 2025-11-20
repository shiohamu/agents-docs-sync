# agents-docs-sync

<!-- MANUAL_START:description -->
## 概要

GitHub にプッシュされた変更をトリガーに、テスト実行・ドキュメント生成・AGENTS.md の自動更新を行うパイプライン
<!-- MANUAL_END:description -->

## 使用技術

- Python
- JavaScript
- Shell

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

## プロジェクト構造

```
.github/
  workflows/
agents_docs_sync.egg-info/
  dependency_links.txt
  entry_points.txt
  requires.txt
  SOURCES.txt
  top_level.txt
docgen/
  collectors/
  detectors/
  generators/
  hooks/
  utils/
docs/
  implementation/
  review/
    README.md
  api.md
  DEVELOPER_GUIDE.md
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-20 10:34:13*
