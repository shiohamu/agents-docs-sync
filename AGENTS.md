# AGENTS ドキュメント

自動生成日時: 2025-11-25 17:13:11

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->
このプロジェクトは、**agents-docs-sync** と呼ばれる CI パイプラインを提供します。  
各コミット時に以下の処理が自動的に実行されます。

- **テスト実行**：Python の `pytest`（pyyaml, pytest-cov, pytest-mock 依存）と、必要なら npm を利用した JavaScript テスト (`npm test`) が走ります。  
- **ドキュメント生成**：`docgen/docgen.py` スクリプトを実行し、YAML 定義から API ドキュメントやサンプルコード等を自動で作成します。このスクリプトは `uv run python3 docgen/docgen.py` というビルドコマンドで呼び出されます。  
- **AGENTS.md の更新**：生成された情報に基づき、リポジトリ内の AGENTS.md を自動的に再構築します。このファイルはエージェント一覧とその仕様をまとめた中心的なドキュメントです。

使用言語・ツール  
- **Python & Shell**：メインロジック（docgen スクリプト）およびビルド/テストスクリプト。  
- **uv**：仮想環境管理とパッケージ実行に利用。`uv run pytest`, `uv run python3 docgen/docgen.py` などで一貫した依存解決を保証します。

主な依存ライブラリ（Python）  

| ライブラリ | バージョン要件 |
|------------|----------------|
| pyyaml     | >=6.0.3        |
| pytest     | >=7.4.0        |
| pytest-cov | >=4.1.0        |
| pytest-mock| >=3.11.1       |

ビルド／テストコマンド  
- ビルド: `uv run python3 docgen/docgen.py`  
- テスト (Python): `uv run pytest`, `uv run pytest tests/ -v --tb=short`  
- テスト (JavaScript): `npm test`

**コード品質管理**：リントツールとして **ruff** を採用し、スタイルと静的解析を一括で実行します。  

このパイプラインにより、エージェントの仕様変更がコミットされるたびにテスト失敗やドキュメント不整合を即座に検知・修正でき、開発者は最新かつ正確な情報だけを手元で確認できます。
<!-- MANUAL_END:description -->

**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->
### 前提条件

- Python 3.12以上



### 依存関係のインストール


#### Python依存関係

```bash

uv sync

```






### LLM環境のセットアップ




#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - Ollamaをインストール: https://ollama.ai/
   - モデルをダウンロード: `ollama pull llama3`
   - サービスを起動: `ollama serve`

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください
<!-- MANUAL_END:setup -->

---

## ビルドおよびテスト手順

<!-- MANUAL_START:usage -->
### ビルド手順


ビルド手順は設定されていません。


### テスト実行


テストコマンドは設定されていません。
<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   
   # テストコマンドを実行
   
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:other -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   
   # テストコマンドを実行
   
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:other -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 17:13:11*


---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 17:13:11*
