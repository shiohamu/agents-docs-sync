# ステップ5: 統合パイプラインスクリプトの作成

## 目的

テスト実行→ドキュメント生成→AGENTS.md更新を順次実行するスクリプトを作成します。

## 作業内容

### 1. `scripts/run_pipeline.sh`を作成

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== 統合パイプライン開始 ==="

# ステップ1: テスト実行
echo "[1/3] テスト実行中..."
"$SCRIPT_DIR/run_tests.sh"
if [ $? -ne 0 ]; then
    echo "エラー: テストが失敗しました"
    exit 1
fi

# ステップ2: ドキュメント生成
echo "[2/3] ドキュメント生成中..."
cd "$PROJECT_ROOT"
python3 docgen/docgen.py
if [ $? -ne 0 ]; then
    echo "エラー: ドキュメント生成が失敗しました"
    exit 1
fi

# ステップ3: 完了
echo "[3/3] パイプライン完了"
echo "=== 統合パイプライン終了 ==="
```

### 2. 実行権限を付与

```bash
chmod +x scripts/run_pipeline.sh
```

## 確認事項

- [ ] スクリプトが正常に実行されるか
- [ ] 各ステップが順番に実行されるか
- [ ] エラーハンドリングが適切か
  ```bash
  ./scripts/run_pipeline.sh
  ```

## 次のステップ

このステップが完了したら、[ステップ6: GitHub Actionsワークフローの作成](./step6-github-actions.md)に進んでください。

