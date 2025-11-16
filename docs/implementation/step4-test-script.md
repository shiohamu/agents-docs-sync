# ステップ4: テスト実行スクリプトの作成

## 目的

テスト実行を標準化し、CI/CDで使用できるスクリプトを作成します。

## 作業内容

### 1. `scripts/`ディレクトリを作成（存在しない場合）

```bash
mkdir -p scripts
```

### 2. `scripts/run_tests.sh`を作成

```bash
#!/bin/bash
set -e

echo "=== テスト実行開始 ==="

# 仮想環境の確認（オプション）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# pytestでテスト実行
pytest tests/ -v --tb=short

echo "=== テスト実行完了 ==="
```

### 3. 実行権限を付与

```bash
chmod +x scripts/run_tests.sh
```

## 確認事項

- [ ] スクリプトが実行可能か
- [ ] ローカルでテストが正常に実行されるか
  ```bash
  ./scripts/run_tests.sh
  ```

## 次のステップ

このステップが完了したら、[ステップ5: 統合パイプラインスクリプトの作成](./step5-pipeline-script.md)に進んでください。

