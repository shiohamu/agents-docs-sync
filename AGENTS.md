# AGENTS ドキュメント

自動生成日時: 2025-11-16 17:43:36

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

**使用技術**: python, javascript, shell

---

## 開発環境のセットアップ

### 前提条件

- Python 3.12以上
- Node.js 18以上

### 依存関係のインストール

#### Python依存関係

```bash
pip install -r requirements-docgen.txt
pip install -r requirements-test.txt
```

### LLM環境のセットアップ

#### APIを使用する場合

1. **APIキーの取得と設定**

   - OpenAI APIキーを取得: https://platform.openai.com/api-keys
   - 環境変数に設定: `export OPENAI_API_KEY=your-api-key-here`

2. **API使用時の注意事項**
   - APIレート制限に注意してください
   - コスト管理のために使用量を監視してください

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
python3 .docgen/docgen.py
```

### テスト実行

#### APIを使用する場合

```bash
pytest
python3 -m pytest test
pytest tests/ -v --tb=short
```

#### ローカルLLMを使用する場合

```bash
pytest
python3 -m pytest test
pytest tests/ -v --tb=short
```

**注意**: ローカルLLMを使用する場合、テスト実行前にモデルが起動していることを確認してください。



---

## コーディング規約

コーディング規約は自動検出されませんでした。プロジェクトの規約に従ってください。


---

## プルリクエストの手順

1. **ブランチの作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **変更のコミット**
   - コミットメッセージは明確で説明的に
   - 関連するIssue番号を含める

3. **テストの実行**
   ```bash
   pytest
   python3 -m pytest test
   pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このドキュメントは自動生成されています。最終更新: 2025-11-16 17:43:36*
