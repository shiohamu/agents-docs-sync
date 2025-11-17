#!/bin/bash
#
# Gitフックを手動でインストールするスクリプト
#

set -e

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$PROJECT_ROOT" ]; then
    echo "エラー: Gitリポジトリ内で実行してください"
    exit 1
fi

cd "$PROJECT_ROOT"

GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
DOCGEN_DIR="$PROJECT_ROOT/.docgen"

if [ ! -d "$GIT_HOOKS_DIR" ]; then
    mkdir -p "$GIT_HOOKS_DIR"
fi

install_hook() {
    local hook_name=$1
    local hook_file="$GIT_HOOKS_DIR/$hook_name"
    local source_file="$DOCGEN_DIR/hooks/$hook_name"

    if [ ! -f "$source_file" ]; then
        echo "警告: $hook_name フックのソースファイルが見つかりません: $source_file"
        return 1
    fi

    # 既存のフックをバックアップ
    if [ -f "$hook_file" ] && ! grep -q "# docgen" "$hook_file" 2>/dev/null; then
        BACKUP_FILE="${hook_file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$hook_file" "$BACKUP_FILE"
        echo "既存の$hook_nameフックをバックアップしました: $BACKUP_FILE"
    fi

    # フックを追加
    if ! grep -q "# docgen" "$hook_file" 2>/dev/null; then
        # シェバンが存在しない場合は追加
        if [ ! -f "$hook_file" ] || ! head -1 "$hook_file" | grep -q "^#!"; then
            echo "#!/bin/bash" > "$hook_file"
        fi
        {
            echo ""
            echo "# docgen - $hook_name hook"
            if [ "$hook_name" = "post-commit" ]; then
                echo "# このフックはデフォルトで無効です。有効にするには環境変数を設定してください:"
                echo "# export DOCGEN_ENABLE_POST_COMMIT=1"
            elif [ "$hook_name" = "pre-push" ]; then
                echo "# このフックはデフォルトで無効です。有効にするには環境変数を設定してください:"
                echo "# export AUTO_RELEASE_ENABLED=1"
            fi
            cat "$source_file"
        } >> "$hook_file"
        chmod +x "$hook_file"
        echo "✓ $hook_nameフックをインストールしました"
        return 0
    else
        echo "✓ $hook_nameフックは既にインストールされています"
        return 0
    fi
}

echo "Gitフックをインストール中..."
install_hook "pre-commit"
install_hook "post-commit"
install_hook "pre-push"

echo ""
echo "インストール完了！"
echo ""
echo "使用方法:"
echo "  - pre-commit: 自動的に実行されます"
echo "  - post-commit: export DOCGEN_ENABLE_POST_COMMIT=1 で有効化"
echo "  - pre-push: export AUTO_RELEASE_ENABLED=1 で有効化"

