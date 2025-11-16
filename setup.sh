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
DOCGEN_DIR="$PROJECT_ROOT/.docgen"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

info "汎用ドキュメント自動生成システムのセットアップを開始します"
info "プロジェクトルート: $PROJECT_ROOT"

# 1. 環境チェック
info "環境をチェック中..."

# uvの確認
if ! command -v uv &> /dev/null; then
    error "uvが見つかりません。"
    error "uvをインストールしてください: curl -LsSf https://astral.sh/uv/install.sh | sh"
    error "または: pip install uv"
    exit 1
fi

UV_VERSION=$(uv --version 2>&1 | head -1)
info "uv バージョン: $UV_VERSION"

# Python 3の確認（uvが自動で管理するが、確認のため）
if ! command -v python3 &> /dev/null && ! uv python list &> /dev/null; then
    warn "Python 3が見つかりません。uvが自動でインストールします。"
else
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' 2>/dev/null || uv run python3 --version 2>&1 | awk '{print $2}')
    if [ -n "$PYTHON_VERSION" ]; then
        info "Python バージョン: $PYTHON_VERSION"
    fi
fi

# Gitの確認
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

# 2. 必要なPythonパッケージの確認とインストール
info "必要なPythonパッケージをチェック中..."

# requirements.txtまたはpyproject.tomlがあるか確認
REQUIREMENTS_FILE=""
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"
elif [ -f "$PROJECT_ROOT/pyproject.toml" ]; then
    REQUIREMENTS_FILE="$PROJECT_ROOT/pyproject.toml"
fi

# docgen用の依存関係をチェック
check_package() {
    uv run python3 -c "import $1" 2>/dev/null
}

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

# 3. .docgenディレクトリの確認
if [ ! -d "$DOCGEN_DIR" ]; then
    error ".docgenディレクトリが見つかりません。"
    error "このスクリプトは、.docgenディレクトリが存在するプロジェクトで実行してください。"
    exit 1
fi

info ".docgenディレクトリを確認しました"

# 4. docgen.pyの実行権限を確認
DOCGEN_SCRIPT="$DOCGEN_DIR/docgen.py"
if [ -f "$DOCGEN_SCRIPT" ]; then
    chmod +x "$DOCGEN_SCRIPT" 2>/dev/null || true
    info "docgen.pyの実行権限を設定しました"
else
    error "docgen.pyが見つかりません"
    exit 1
fi

# 5. Git hooksのインストール
if [ "$GIT_AVAILABLE" = true ]; then
    info "Git hooksをインストール中..."

    if [ ! -d "$GIT_HOOKS_DIR" ]; then
        mkdir -p "$GIT_HOOKS_DIR"
    fi

    # pre-commitフックのインストール
    PRE_COMMIT_HOOK="$GIT_HOOKS_DIR/pre-commit"
    PRE_COMMIT_SOURCE="$DOCGEN_DIR/hooks/pre-commit"

    if [ -f "$PRE_COMMIT_SOURCE" ]; then
        # 既存のpre-commitフックをバックアップ
        if [ -f "$PRE_COMMIT_HOOK" ] && ! grep -q "# docgen" "$PRE_COMMIT_HOOK" 2>/dev/null; then
            BACKUP_FILE="${PRE_COMMIT_HOOK}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$PRE_COMMIT_HOOK" "$BACKUP_FILE"
            info "既存のpre-commitフックをバックアップしました: $BACKUP_FILE"
        fi

        # docgenのpre-commitフックを追加
        if ! grep -q "# docgen" "$PRE_COMMIT_HOOK" 2>/dev/null; then
            {
                echo ""
                echo "# docgen - ドキュメント自動生成フック"
                echo "# 以下の行を削除すると、docgenのpre-commitフックが無効になります"
                cat "$PRE_COMMIT_SOURCE"
            } >> "$PRE_COMMIT_HOOK"
            chmod +x "$PRE_COMMIT_HOOK"
            info "pre-commitフックをインストールしました"
        else
            info "pre-commitフックは既にインストールされています"
        fi
    else
        warn "pre-commitフックのソースファイルが見つかりません: $PRE_COMMIT_SOURCE"
    fi

    # post-commitフックのインストール（オプション）
    POST_COMMIT_HOOK="$GIT_HOOKS_DIR/post-commit"
    POST_COMMIT_SOURCE="$DOCGEN_DIR/hooks/post-commit"

    if [ -f "$POST_COMMIT_SOURCE" ]; then
        if [ -f "$POST_COMMIT_HOOK" ] && ! grep -q "# docgen" "$POST_COMMIT_HOOK" 2>/dev/null; then
            BACKUP_FILE="${POST_COMMIT_HOOK}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$POST_COMMIT_HOOK" "$BACKUP_FILE"
            info "既存のpost-commitフックをバックアップしました: $BACKUP_FILE"
        fi

        if ! grep -q "# docgen" "$POST_COMMIT_HOOK" 2>/dev/null; then
            {
                echo ""
                echo "# docgen - ドキュメント自動生成フック（オプション）"
                echo "# このフックはデフォルトで無効です。有効にするには環境変数を設定してください:"
                echo "# export DOCGEN_ENABLE_POST_COMMIT=1"
                cat "$POST_COMMIT_SOURCE"
            } >> "$POST_COMMIT_HOOK"
            chmod +x "$POST_COMMIT_HOOK"
            info "post-commitフックをインストールしました（デフォルトは無効）"
        else
            info "post-commitフックは既にインストールされています"
        fi
    fi
else
    warn "Gitリポジトリでないため、Git hooksはインストールされませんでした"
fi

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

