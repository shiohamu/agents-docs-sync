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

#### 方法1: uvを使用する場合（推奨）

```bash
# セットアップスクリプトを実行
./setup.sh
```

#### 方法2: pipを使用する場合

```bash
# ドキュメント生成システム用の依存関係
pip install -r requirements-docgen.txt

# テスト用の依存関係
pip install -r requirements-test.txt
```

#### 方法3: pyproject.tomlからインストール

```bash
pip install -e .
```

### 初回設定

初回実行時は、`.docgen/config.yaml`が自動的に作成されます（`config.yaml.sample`からコピーされます）。

手動で設定ファイルを作成する場合:

```bash
cp .docgen/config.yaml.sample .docgen/config.yaml
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
├── pytest.ini
...
```

---

*このREADMEは自動生成されています。最終更新: 2025-11-16 15:54:52*
