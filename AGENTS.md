# AGENTS ドキュメント

自動生成日時: 2025-11-18 12:50:37

このドキュメントは、AIコーディングエージェントがプロジェクト内で効果的に作業するための指示とコンテキストを提供します。

---

## プロジェクト概要

<!-- MANUAL_START:description -->

**PROJECT NAME:** agents-docs-sync

**使用技術 (Use languages): Python, JavaScript, Shell**

**依存関係**

- pyyaml >=6.0.3
- pytest >=7.4.0
- pytest-cov >=4.1.0
- pytest-mock >=3.11.1

このプロジェクトは、`agents-docs-sync`というドキュメント自動生成・同期システムです。AIコーディングエージェントがプロジェクトで効果的に作業するための`AGENTS.md`ドキュメントを自動生成・更新します。

**主な機能**:
- プロジェクト情報の自動収集と分析
- `AGENTS.md`と`README.md`の自動生成・更新
- GitHub Actionsによる自動化パイプライン
- ローカルLLMとAPI LLMの両方に対応

**ビルドコマンド**

```bash
python3 docgen/docgen.py
```

**テストコマンド**

- `python3 -m pytest tests`
- `pytest` (default)
- `pytest tests/ -v --tb=short`

**GitHub Actions**:
- pushイベント時に自動的にテストを実行
- ドキュメントの自動更新
- CI/CDパイプラインによる継続的インテグレーション

**テスト実行**:
- `pytest tests/ -v --tb=short` コマンドでテストを実行
- ローカルLLM使用時は、モデルが起動していることを確認

<!-- MANUAL_END:description -->

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

#### ローカルLLMを使用する場合

1. **ローカルLLMのインストール**

   - LM Studioをインストール: https://lmstudio.ai/
   - モデルをダウンロードして起動
   - ベースURL: http://192.168.10.113:1234

2. **ローカルLLM使用時の注意事項**
   - モデルが起動していることを確認してください
   - ローカルリソース（メモリ、CPU）を監視してください


---

## ビルドおよびテスト手順

### ビルド手順

```bash
python3 docgen/docgen.py
```

### テスト実行

#### ローカルLLMを使用する場合

```bash
python3 -m pytest test
pytest
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
   python3 -m pytest test
   pytest
   pytest tests/ -v --tb=short
   ```

4. **プルリクエストの作成**
   - タイトル: `[種類] 簡潔な説明`
   - 説明: 変更内容、テスト結果、関連Issueを記載


---

*このドキュメントは自動生成されています。最終更新: 2025-11-18 12:50:37*
