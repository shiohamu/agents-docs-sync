# AGENTS ドキュメント

自動生成日時: 2025-11-25 18:38:58

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

本プロジェクトは、Python と Shell スクリプトで構成された CI/CD パイプラインを提供し、リポジトリにコミットが行われるたびに以下の処理を自動実行します。

- **ビルド**：`uv sync` で依存関係をインストールし、`uv build` でプロジェクトを構築。  
- **テスト実行**：Python は `pytest`, Node.js は `npm test`, Go は `go test ./...` を用いて統合的に検証します（カバレッジ報告は pytest-cov が担当）。  
- **ドキュメント生成 & AGENTS.md 更新**：`uv run python3 docgen/docgen.py` で最新の API ドキュメントを作成し、AGENTS.md を自動的に同期します。  

依存パッケージは `pyyaml>=6.0.3, pytest>=7.4.0, pytest-cov>=4.1.0, pytest-mock>=3.11.1` のみで構成されており、環境設定がシンプルです。  
コーディング規約には `ruff` を採用し、一貫したコード品質を保証します。  

このワークフローにより、ドキュメントの鮮度とテストカバレッジを常に最新状態で保ちつつ、人手による更新作業を大幅に削減できます。

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


['uv sync', 'uv build', 'uv run python3 docgen/docgen.py']


### テスト実行



#### APIを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
uv run pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
npm test
```

#### ローカルLLMを使用する場合

```bash
npm test
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。

#### APIを使用する場合

```bash
go test ./...
```

#### ローカルLLMを使用する場合

```bash
go test ./...
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。
<!-- MANUAL_END:usage -->

---

## コーディング規約

<!-- MANUAL_START:other -->
### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```
<!-- MANUAL_END:other -->

---

## プルリクエストの手順

<!-- MANUAL_START:pr -->
1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   
   
   uv run pytest tests/ -v --tb=short
   
   npm test
   
   go test ./...
   
   
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載
<!-- MANUAL_END:pr -->



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 18:38:58*