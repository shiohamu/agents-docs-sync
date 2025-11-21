# agents-docs-sync

<!-- MANUAL_START:description -->

## 概要

`agents-docs-sync` は、GitHub Actions を活用したマルチ言語 CI/CD パイプラインです。  
リポジトリへコードが `push` されるたびに自動で以下の処理を実行し、品質保証とドキュメント整合性を継続的に保ちます。

1. **ビルド・テスト**  
   - **Python**：`pytest + coverage.py` によってユニット/統合テストを実施。カバレッジ結果は自動で報告され、PR へのコメントとして表示します。  
   - **JavaScript / TypeScript**：`jest` を使用し同等のテストを走らせます。またスナップショットとコードカバー率も確認。  
   - **C/C++**：Google Test 等で単体テストを実行、さらに `clang-tidy`, `cppcheck` などによる静的解析でビルドエラー・品質問題の検出に努めます。

2. **API ドキュメント自動生成**  
   - **Python**：Sphinx を利用し docstring から Markdown / HTML の API リファレンス (`docs/python/`) を作成。  
   - **JavaScript**：JSDoc／TypeDoc により `docs/javascript/` 内に整形済みの HTML ドキュメントを生成。  
   - **C**：Doxygen でコメントベースの API 文書（`docs/c/`）を出力し、ビルド時に更新します。

3. **AGENTS.md の自動更新**  
   各言語ごとのテスト結果と生成されたドキュメントへのリンクからエージェント一覧・稼働状態を抽出。  
   これら情報は `AGENTS.md` に差分コミットされ、メンテナがいつでも最新のステータスを確認できるようになります。

4. **成果物公開**  
   - `docs/` ディレクトリ全体を GitHub Pages 等へ自動デプロイ。必要なトークンスコープは事前に設定済みです。  

### 主なメリット

| 項目 | 具体的価値 |
|------|------------|
| **継続的インテグレーション** | コード変更ごとに検証・ドキュメント生成され、品質低下を早期発見できます。 |
| **一元管理** | 複数言語のエージェント情報や API 仕様が統合された `AGENTS.md` に集約されます。 |
| **リソース効率化** | Actions のスケジューリングと最適なジョブ構成でビルド時間・コストを削減します。 |

このパイプラインにより、開発者はコード変更だけではなく、その影響範囲（テスト結果や最新ドキュメント）まで一貫して追跡できるようになります。


<!-- 手動で追加・編集する場合はこちらへ記載してください。 -->

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

*このREADMEは自動生成されています。最終更新: 2025-11-21 12:40:07*
