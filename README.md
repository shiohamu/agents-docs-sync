# agents-docs-sync


## 概要

<!-- MANUAL_START:description -->
**agents‑docs-sync** は、Python・JavaScript（TypeScript もサポート）と C の三言語で構築された軽量 CI/CD パイプラインです。
AI コーディングエージェントがプロジェクトを迅速に理解し協調できるよう設計されており、コード変更時のテスト実行・ドキュメント生成／同期を自動化します。

### 主な機能

- **CI での自動テスト**
  - *Python*：`pytest` によるユニット/統合テスト。カバレッジ計測は `coverage.py` をオプションで有効にできます。
  - *JavaScript / TypeScript*：Jest／Mocha を利用し、フロントエンド・バックエンド両方を網羅します。型チェックには `tsc --noEmit` が組み込まれています。
  - *C*：GCC/Clang のビルド＋テストスイート（`make test` 等）で実行し、静的解析ツールの結果もレポートします。

- **ドキュメント自動同期**
  `AGENTS.md` と `README.md` をコードベースと連携させてライブラリバージョン・API エンドポイントなどメタ情報を常に最新化。手作業による更新ミスや古い説明文を排除します。

- **GitHub Actions 統合**
  プッシュイベントでワークフローが起動し、ビルド→テスト→同期という一連処理を並列実行。CI の失敗時は即座に通知されます。

- **LLM 対応（ローカル・API ベース）**
  - *ローカル LLM*：LM Studio, Ollama 等での利用が可能です。
  - *クラウド API*：OpenAI, Anthropic などをサポートし、モデル固有の出力スキーマに従いながらドキュメント生成やコードコメント補完を行います。

- **Outlines ライブラリ利用**
  スキーマ保証付き JSON/YAML 出力でドキュメント構造が整合性保持。実験的ですが高い安定性と再現性を提供します。

### ワークフロー

1. GitHub Actions が新しいコミットを検知
2. Python・JavaScript・C のテストスイートを並列で実行し品質保証
3. 成功時に `AGENTS.md` を最新のエージェント仕様へ更新
4. 変更内容を元に `README.md` とその他ドキュメントを自動生成／同期

### 利点

- **高速なデプロイ**：手作業なしでドキュメントが常時最新版。
- **品質保証**：テスト失敗時はビルド停止し、エラー箇所を即座に把握。
- **AI エージェントの効率化**：最新情報とスクリプトが自動で提供されるため、開発者・研究者が AI に頼らずとも迅速なタスク実行可能。

このパイプラインはプロジェクト全体を常に整合性ある状態に保ちつつ、人間の手作業負担を大幅に軽減します。
<!-- MANUAL_END:description -->

## 使用技術

- Python
- JavaScript
- C

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.8以上
- Node.js 14以上

### インストール手順

```bash
# Pythonの依存関係をインストール
pip install -r requirements-docgen.txt
pip install -r requirements-test.txt

# Node.jsの依存関係をインストール (必要に応じて)
npm install
```

### LLM環境のセットアップ

#### ローカルLLMを使用する場合

1. **LM Studioのインストール**
   - [LM Studio](https://lmstudio.ai/)をダウンロードしてインストール
   - お好みのモデルをダウンロード
   - サーバーを起動（デフォルト: `http://localhost:1234`）

2. **設定ファイルの編集**
   - `docgen/config.yaml`を編集
   - `llm_mode`を`local`または`both`に設定
   - `local_llm`の`base_url`を確認

#### API LLMを使用する場合

1. **APIキーの設定**
   - 環境変数に APIキーを設定
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # または
   export ANTHROPIC_API_KEY="your-api-key"
   ```

2. **設定ファイルの編集**
   - `docgen/config.yaml`を編集
   - `llm_mode`を`api`または`both`に設定
   - 使用するプロバイダーとモデルを指定
<!-- MANUAL_END:setup -->

## プロジェクト構造

```
├── .github
│   └── workflows
├── agents_docs_sync
├── agents_docs_sync.egg-info
├── docgen
│   ├── detectors
│   ├── generators
│   ├── collectors
│   ├── hooks
│   └── templates
├── docs
│   └── implementation/
├── schemas
├── scripts
├── tests
│   ├── test_collectors
│   ├── test_detectors
│   ├── test_generators
│   ├── test_parsers
│   └── test_utils
...
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-19 10:48:57*
