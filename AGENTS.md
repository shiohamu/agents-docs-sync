# AGENTS ドキュメント

自動生成日時: 2025-11-25 19:09:16

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

**agents-docs-sync** は、コードベースにコミットがあるたびに自動でテストを実行し、ドキュメントを生成して `AGENTS.md` を更新するCI/CDパイプラインです。  
主な特徴は次の通りです。

- **使用言語**: Python（メインロジック）とシェルスクリプト（ビルド・テスト実行用）
- **依存関係**
  - `pyyaml>=6.0.3`：YAML の読み書き
  - `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`：テスト実行とカバレッジ計測、モック機能
- **ビルド手順**
```bash
uv sync          # 依存関係をインストール・同期
uv build         # パッケージのビルド（必要に応じて）
uv run python3 docgen/docgen.py   # ドキュメント生成スクリプト実行
```
- **テスト手順**
```bash
uv run pytest tests/ -v --tb=short  # Python テスト
npm test                                 # JavaScript 用の追加テスト（必要に応じて）
go test ./...                            # Go モジュール用のテスト（必要に応じて）
```
- **コーディング規約**  
  `ruff` を使用した静的解析・フォーマッティングを実施し、コード品質と一貫性を保ちます。

このプロジェクトは継続的インテグレーション環境（GitHub Actions 等）で動作するよう設計されており、新しい機能や修正がコミットされた際に自動でドキュメントの更新と品質保証を行います。

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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-25 19:09:16*