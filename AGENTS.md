# AGENTS ドキュメント

自動生成日時: 2025-11-27 23:24:22

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---


<!-- MANUAL_START:description -->

<!-- MANUAL_END:description -->


agents-docs-sync は、コードベースの変更がコミットされるたびに自動でテストを実行し、ドキュメント（YAML/Markdown）を生成して AGENTS.md を更新する継続的インテグレーションパイプラインです。  
主なフローは次のとおりです。

1. **ビルド** – `uv sync` で Python と Node.js の依存関係を解決し、`uv build` でプロジェクト全体をコンパイル/リンクします。  
2. **テスト実行** – `pytest`（Python）、`npm test`（JavaScript）および `go test ./...` がそれぞれの言語領域でユニット・統合テストを走らせ、失敗した場合はビルドが中断されます。  
3. **ドキュメント生成** – `uv run python3 docgen/docgen.py` を実行してコードベースから最新の API/設定情報を抽出し、AGENTS.md 用に整形します。  
4. **コミット自動化** – 変更が検知されると GitHub Actions（またはローカル CI）で上記ステップが順次実行され、生成された AGENTS.md がリポジトリへプッシュされます。

### 開発者向けのヒント

- **Python 環境**  
  - 必要なパッケージ：`pyyaml>=6.0.3`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `pytest-mock>=3.11.1`
  - コードは Ruff を使用して静的解析・フォーマットを行います。  
- **スクリプト実行**  
  ```bash
  uv sync          # 依存関係のインストール/更新
  uv build         # ビルド（必要に応じて）
  uv run python3 docgen/docgen.py   # ドキュメント生成
  ```
- **テストコマンド**  
  ```bash
  uv run pytest tests/ -v --tb=short      # Python テスト
  npm test                                 # JavaScript テスト
  go test ./...                            # Go テスト（必要に応じて）
  ```

### コントリビューション

1. **変更を加える** – 必要な機能や修正をローカルで実装。  
2. **テストとドキュメントの更新** – 上記コマンドを走らせ、すべてが成功することを確認。  
3. **コミット & プッシュ** – 変更は自動的に CI パイプラインへ送信され、AGENTS.md が最新状態になります。

この仕組みにより、新しいエージェントや設定項目の追加・修正時にドキュメントが常に同期し、人手による更新ミスを防止します。
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

*このAGENTS.mdは自動生成されています。最終更新: 2025-11-27 23:24:22*