#!/bin/bash
#
# 汎用ドキュメント自動生成システム セットアップスクリプト
# このスクリプトを実行すると、プロジェクトにドキュメント自動更新機能を追加します
#

set -e  # エラーが発生したら終了

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# メッセージ表示関数
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# プロジェクトルートを取得
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCGEN_DIR="$PROJECT_ROOT/docgen"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

# グローバル変数
GIT_AVAILABLE=false

# ============================================
# 環境チェック関数
# ============================================

check_uv() {
    # uvの存在確認
    if ! command -v uv &> /dev/null; then
        error "uvが見つかりません。"
        error "uvをインストールしてください: curl -LsSf https://astral.sh/uv/install.sh | sh"
        error "または: pip install uv"
        exit 1
    fi
    UV_VERSION=$(uv --version 2>&1 | head -1)
    info "uv バージョン: $UV_VERSION"
}

check_python() {
    # Python 3の存在確認
    if ! command -v python3 &> /dev/null && ! uv python list &> /dev/null; then
        warn "Python 3が見つかりません。uvが自動でインストールします。"
    else
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' 2>/dev/null || uv run python3 --version 2>&1 | awk '{print $2}')
        if [ -n "$PYTHON_VERSION" ]; then
            info "Python バージョン: $PYTHON_VERSION"
        fi
    fi
}

check_git() {
    # Gitの存在確認とリポジトリチェック
    if ! command -v git &> /dev/null; then
        warn "Gitが見つかりません。Gitリポジトリでない場合、Git hooksはインストールされません。"
        GIT_AVAILABLE=false
    else
        GIT_AVAILABLE=true
        info "Git が見つかりました"

        # Gitリポジトリか確認
        if ! git rev-parse --git-dir > /dev/null 2>&1; then
            warn "このディレクトリはGitリポジトリではありません。Git hooksはインストールされません。"
            GIT_AVAILABLE=false
        else
            info "Gitリポジトリとして認識されました"
        fi
    fi
}

check_environment() {
    # 環境チェックを実行
    info "環境をチェック中..."
    check_uv
    check_python
    check_git
}

# ============================================
# メイン処理
# ============================================

info "汎用ドキュメント自動生成システムのセットアップを開始します"
info "プロジェクトルート: $PROJECT_ROOT"

# 1. 環境チェック
check_environment

# ============================================
# 依存関係チェック関数
# ============================================

check_package() {
    # パッケージの存在確認
    uv run python3 -c "import $1" 2>/dev/null
}

check_and_install_packages() {
    # 必要なPythonパッケージの確認とインストール
    info "必要なPythonパッケージをチェック中..."

    MISSING_PACKAGES=()

    if ! check_package yaml; then
        MISSING_PACKAGES+=("PyYAML")
    fi

    if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
        warn "以下のパッケージが見つかりません: ${MISSING_PACKAGES[*]}"
        read -p "インストールしますか？ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "uv pip install ${MISSING_PACKAGES[*]} を実行中..."
            uv pip install "${MISSING_PACKAGES[@]}" || {
                error "パッケージのインストールに失敗しました"
                exit 1
            }
            info "パッケージのインストールが完了しました"
        else
            warn "パッケージがインストールされていません。後で手動でインストールしてください:"
            echo "  uv pip install ${MISSING_PACKAGES[*]}"
        fi
    else
        info "必要なパッケージはすべてインストールされています"
    fi
}

# 2. 必要なPythonパッケージの確認とインストール
check_and_install_packages

# 3. docgenディレクトリの確認
if [ ! -d "$DOCGEN_DIR" ]; then
    error "docgenディレクトリが見つかりません。"
    error "このスクリプトは、docgenディレクトリが存在するプロジェクトで実行してください。"
    exit 1
fi

info "docgenディレクトリを確認しました"

# 4. docgen.pyの実行権限を確認
DOCGEN_SCRIPT="$DOCGEN_DIR/docgen.py"
if [ -f "$DOCGEN_SCRIPT" ]; then
    chmod +x "$DOCGEN_SCRIPT" 2>/dev/null || true
    info "docgen.pyの実行権限を設定しました"
else
    error "docgen.pyが見つかりません"
    exit 1
fi

# ============================================
# Git hooksインストール関数
# ============================================

install_git_hook() {
    # Gitフックをインストール
    local hook_name=$1
    local hook_file="$GIT_HOOKS_DIR/$hook_name"
    local source_file="$DOCGEN_DIR/hooks/$hook_name"
    local hook_description=$2

    if [ ! -f "$source_file" ]; then
        warn "$hook_name フックのソースファイルが見つかりません: $source_file"
        return 1
    fi

    # 既存のフックをバックアップ
    if [ -f "$hook_file" ] && ! grep -q "# docgen" "$hook_file" 2>/dev/null; then
        BACKUP_FILE="${hook_file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$hook_file" "$BACKUP_FILE"
        info "既存の$hook_nameフックをバックアップしました: $BACKUP_FILE"
    fi

    # フックを追加
    if ! grep -q "# docgen" "$hook_file" 2>/dev/null; then
        # シェバンが存在しない場合は追加
        if [ ! -f "$hook_file" ] || ! head -1 "$hook_file" | grep -q "^#!"; then
            echo "#!/bin/bash" > "$hook_file"
        fi
        {
            echo ""
            echo "# docgen - $hook_description"
            if [ "$hook_name" = "post-commit" ]; then
                echo "# このフックはデフォルトで無効です。有効にするには環境変数を設定してください:"
                echo "# export DOCGEN_ENABLE_POST_COMMIT=1"
            elif [ "$hook_name" = "pre-push" ]; then
                echo "# このフックはデフォルトで無効です。有効にするには環境変数を設定してください:"
                echo "# export AUTO_RELEASE_ENABLED=1"
            else
                echo "# 以下の行を削除すると、docgenの$hook_nameフックが無効になります"
            fi
            cat "$source_file"
        } >> "$hook_file"
        chmod +x "$hook_file"
        info "$hook_nameフックをインストールしました"
        return 0
    else
        info "$hook_nameフックは既にインストールされています"
        return 0
    fi
}

install_git_hooks() {
    # Git hooksをインストール
    if [ "$GIT_AVAILABLE" != true ]; then
        warn "Gitリポジトリでないため、Git hooksはインストールされませんでした"
        return 1
    fi

    info "Git hooksをインストール中..."

    if [ ! -d "$GIT_HOOKS_DIR" ]; then
        mkdir -p "$GIT_HOOKS_DIR"
    fi

    install_git_hook "pre-commit" "ドキュメント自動生成フック"
    install_git_hook "post-commit" "ドキュメント自動生成フック（オプション）"
    install_git_hook "pre-push" "自動リリースフック（オプション、環境変数 AUTO_RELEASE_ENABLED=1 で有効化）"
    install_git_hook "commit-msg" "コミットメッセージ自動生成フック（LLM使用）"
}

# 5. Git hooksのインストール
install_git_hooks

# 6. 設定ファイルの確認
CONFIG_FILE="$DOCGEN_DIR/config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    warn "設定ファイルが見つかりません: $CONFIG_FILE"
    warn "デフォルト設定が使用されます"
else
    info "設定ファイルを確認しました: $CONFIG_FILE"
fi

# 7. 初回ドキュメント生成（オプション）
echo ""
read -p "初回ドキュメントを生成しますか？ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    info "初回ドキュメントを生成中..."
    cd "$PROJECT_ROOT"
    if uv run python3 "$DOCGEN_SCRIPT"; then
        info "初回ドキュメントの生成が完了しました"
    else
        warn "初回ドキュメントの生成中にエラーが発生しました"
        warn "後で手動で実行できます: uv run python3 $DOCGEN_SCRIPT"
    fi
fi

# 8. セットアップ完了
echo ""
info "=========================================="
info "セットアップが完了しました！"
info "=========================================="
echo ""
info "使用方法:"
echo "  手動実行: uv run python3 $DOCGEN_SCRIPT"
echo "  言語検出のみ: uv run python3 $DOCGEN_SCRIPT --detect-only"
echo ""
if [ "$GIT_AVAILABLE" = true ]; then
    info "Git hooks:"
    echo "  - pre-commit: コミット前に自動実行されます"
    echo "  - post-commit: デフォルトで無効（環境変数 DOCGEN_ENABLE_POST_COMMIT=1 で有効化）"
    echo ""
fi
info "設定ファイル: $CONFIG_FILE"
info "詳細は README.md を参照してください"
echo ""

