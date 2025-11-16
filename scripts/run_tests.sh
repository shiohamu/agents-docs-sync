#!/bin/bash
set -e

echo "=== テスト実行開始 ==="

# 仮想環境の確認（オプション）
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# pytestでテスト実行
python3 -m pytest tests/ -v --tb=short

echo "=== テスト実行完了 ==="

