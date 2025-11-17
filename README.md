# agents-docs-sync

<!-- MANUAL_START:description -->
## 概要

このプロジェクトは、GitHubにプッシュされた変更をトリガーに、テスト実行・ドキュメント生成・AGENTS.mdの自動更新を行うCI/CDパイプラインです。

主な機能:
- プロジェクトの使用言語を自動検出（Python, JavaScript, Goなど）
- APIドキュメントの自動生成
- README.mdの自動更新（手動セクションの保持に対応）
- AGENTS.mdの自動生成（OpenAI仕様準拠、API/ローカルLLM両対応）
- GitHub Actionsによる自動実行
<!-- MANUAL_END:description -->

## 使用技術

- Python
- JavaScript
- Shell

## セットアップ

<!-- MANUAL_START:setup -->
### 必要な環境

- Python 3.12以上
- uv（推奨）またはpip
- Git（Git hooksを使用する場合）
- Bash（スクリプト実行用）
  - Linux/macOS: 標準で利用可能
  - Windows: WSL2、Git Bash、またはMSYS2が必要

### インストール

#### 方法1: PyPIからインストール（推奨）

```bash
# pipを使用する場合
pip install agents-docs-sync

# またはuvを使用する場合
uv pip install agents-docs-sync
```

#### 方法2: ワンライナーインストールスクリプト

```bash
# 最新の安定版をインストール
curl -fsSL https://raw.githubusercontent.com/shiohamu/agents-docs-sync/main/install.sh | bash

# 開発版をインストール（GitHubから）
curl -fsSL https://raw.githubusercontent.com/shiohamu/agents-docs-sync/main/install.sh | bash -s -- --dev
```

#### 方法3: ソースコードからインストール

```bash
# リポジトリをクローン
git clone https://github.com/shiohamu/agents-docs-sync.git
cd agents-docs-sync

# インストール
pip install -e .
```

#### 方法4: uvを使用する場合（開発用）

```bash
# セットアップスクリプトを実行
./setup.sh
```

#### 方法5: 依存関係のみインストール

```bash
# ドキュメント生成システム用の依存関係
pip install -r requirements-docgen.txt

# テスト用の依存関係
pip install -r requirements-test.txt
```

### 初回設定

初回実行時は、`.docgen/config.yaml`が自動的に作成されます（`config.yaml.sample`からコピーされます）。

手動で設定ファイルを作成する場合:

```bash
cp .docgen/config.yaml.sample .docgen/config.yaml
```

### 使用方法

インストール後、以下のコマンドで使用できます：

```bash
# ドキュメントを生成
agents-docs-sync

# 言語検出のみ実行
agents-docs-sync --detect-only

# ヘルプを表示
agents-docs-sync --help

# バージョンを確認
agents-docs-sync --version
```

### Dockerを使用する場合

```bash
# イメージをビルド
docker build -t agents-docs-sync .

# 実行
docker run --rm -v $(pwd):/workspace -w /workspace agents-docs-sync
```

### プラットフォーム対応

- **Linux/macOS**: 完全対応
- **Windows**:
  - WSL2（推奨）: 完全対応
  - Git Bash: スクリプト実行可能
  - MSYS2: スクリプト実行可能
  - ネイティブWindows: Pythonスクリプト（`.docgen/docgen.py`）は直接実行可能、シェルスクリプト（`setup.sh`、`scripts/*.sh`）はWSL2またはGit Bashが必要
<!-- MANUAL_END:setup -->

## プロジェクト構造

```
├── .docgen
│   ├── detectors
│   ├── generators
│   ├── collectors
│   ├── hooks
│   └── templates
├── .github
│   └── workflows
├── agents_docs_sync.egg-info
├── docs
│   └── implementation/
├── scripts
├── tests
│   ├── test_collectors
│   ├── test_detectors
│   ├── test_generators
│   └── test_parsers
├── AGENTS.md
├── README.md
├── pyproject.toml
...
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-17 14:05:26*
