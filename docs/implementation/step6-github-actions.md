# ステップ6: GitHub Actionsワークフローの作成

## 目的

GitHubプッシュ時に自動実行されるCI/CDパイプラインを作成します。

## 作業内容

### 1. `.github/workflows/`ディレクトリを作成

```bash
mkdir -p .github/workflows
```

### 2. `.github/workflows/ci-cd-pipeline.yml`を作成

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt

      - name: Run tests
        run: |
          pytest tests/ -v --tb=short

  generate-docs:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements-docgen.txt

      - name: Generate documents
        run: |
          python3 docgen/docgen.py

      - name: Check for changes
        id: verify-changed-files
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "changed=true" >> $GITHUB_OUTPUT
          else
            echo "changed=false" >> $GITHUB_OUTPUT
          fi

      - name: Commit changes (optional)
        if: steps.verify-changed-files.outputs.changed == 'true' && github.event_name == 'push'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/ README.md AGENTS.md
          git commit -m "docs: auto-update documentation [skip ci]" || exit 0
          git push || exit 0
```

## 確認事項

- [ ] YAMLの構文が正しいか
- [ ] トリガー条件が適切か
- [ ] ジョブの依存関係が正しいか（`generate-docs`は`test`の後に実行）
- [ ] 自動コミットが適切に設定されているか

## 注意事項

- **依存関係のインストール**: `requirements-docgen.txt`を使用することで、docgenシステムに必要な依存関係のみがインストールされます。将来の拡張に備えて、このファイルに新しい依存関係を追加できます。
- 自動コミット機能を使用する場合、リポジトリの設定で適切な権限が必要です
- `[skip ci]`タグにより、自動コミットが新しいワークフローをトリガーしないようにしています
- プルリクエスト時は自動コミットを実行しません（`github.event_name == 'push'`条件）

### 依存関係ファイルの管理

`requirements-docgen.txt`は、docgenシステム専用の依存関係を管理するファイルです。新しい機能を追加する際は、このファイルに必要な依存関係を追加してください。

## 次のステップ

このステップが完了したら、[ステップ7: ローカルでの動作確認](./step7-local-testing.md)に進んでください。

