# AGENTS ドキュメント

自動生成日時: 2025-11-27 13:24:44

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、コードベースのコミットごとに自動的にテストを実行し、ドキュメントを生成して `AGENTS.md` を更新する CI/CD パイプラインです。  
Python と Shell で構成されており、以下が主な特徴となります。

- **ビルド・デプロイ**:  
  - `uv sync`: 必要な Python ライブラリをインストールします（`pyyaml`, `pytest`, `pytest‑cov`, `pytest-mock`）。  
  - `uv build`: プロジェクトのパッケージング。  
  - `uv run python3 docgen/docgen.py`: ドキュメント生成スクリプトを実行し、最新の API 情報やエージェント定義を Markdown に落とします。

- **テスト**:  
  - Python テストは `uv run pytest tests/`（詳細レポート付き）で走査。  
  - JavaScript のユニットテストは `npm test`、Go モジュールのテストは `go test ./...` が呼び出されます。

- **コード品質**:  
  - 全ての Python コードに対して Ruff を使ったスタイルチェックが実施。Lint エラーや警告を事前に検知し、コミット時点でのクリーンな状態を保ちます。

- **自動更新プロセス**:  
  1. GitHub Actions（または同等）から `push` イベントがトリガー。  
  2. 上記ビルド・テストステップ実行後、`docgen.py` が最新のエージェント情報を取得し、Markdown を生成します。  
  3. 変更差分があれば自動で `AGENTS.md` にコミットされます。

- **利用者向け**:  
  - 新しいエージェントやパラメータを追加する際は、関連テストとドキュメントの更新だけを忘れずに。CI が失敗した場合、該当ファイルが指摘されるため修正箇所が明確です。  
  - `uv` を使うことで仮想環境管理や依存関係解決が簡潔になり、ローカルでの開発もスムーズに行えます。

この構成を理解しておくと、エージェント追加・改修時に必要な手順（テスト作成 → コード実装 → ドキュメント更新）が一目瞭然になり、CI が自動で検証・反映するため開発サイクルが高速化します。
**使用技術**: python, shell

---

## 開発環境のセットアップ

<!-- MANUAL_START:setup -->

<!-- MANUAL_END:setup -->
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


---


## ビルドおよびテスト手順

### ビルド手順


```bash
uv sync
uv build
uv run python3 docgen/docgen.py
```


### テスト実行


```bash
uv run pytest tests/ -v --tb=short
npm test
go test ./...
```


---

## コーディング規約

<!-- MANUAL_START:other -->

<!-- MANUAL_END:other -->



### リンター

- **ruff** を使用

  ```bash
  ruff check .
  ruff format .
  ```





---

## プルリクエストの手順

<!-- MANUAL_START:pr -->

<!-- MANUAL_END:pr -->
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



---

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 13:24:44*