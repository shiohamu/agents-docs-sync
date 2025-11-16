#!/bin/bash
#
# agents-docs-sync ワンライナーインストールスクリプト
# このスクリプトは、PyPIからagents-docs-syncをインストールします
#

set -e

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

section() {
    echo -e "${BLUE}===${NC} $1 ${BLUE}===${NC}"
}

# インストール方法の選択
INSTALL_METHOD="pypi"
if [ "$1" = "--dev" ] || [ "$1" = "-d" ]; then
    INSTALL_METHOD="github"
    info "開発版をGitHubからインストールします"
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dev, -d     GitHubから開発版をインストール"
    echo "  --help, -h    このヘルプを表示"
    echo ""
    echo "デフォルトではPyPIから最新の安定版をインストールします"
    exit 0
else
    info "PyPIから最新版をインストールします"
fi

section "環境チェック"

# Pythonの確認
if ! command -v python3 &> /dev/null; then
    error "Python 3が見つかりません"
    error "Python 3.12以上をインストールしてください: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
info "Python バージョン: $PYTHON_VERSION"

# Python 3.12以上か確認
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    error "Python 3.12以上が必要です（現在: $PYTHON_VERSION）"
    exit 1
fi

# pipまたはuvの確認
PIP_CMD=""
if command -v uv &> /dev/null; then
    PIP_CMD="uv pip"
    UV_VERSION=$(uv --version 2>&1 | head -1)
    info "uv が見つかりました: $UV_VERSION"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    info "pip3 が見つかりました: $PIP_VERSION"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    PIP_VERSION=$(pip --version 2>&1 | awk '{print $2}')
    info "pip が見つかりました: $PIP_VERSION"
else
    error "pipまたはuvが見つかりません"
    error "pipをインストールしてください: python3 -m ensurepip --upgrade"
    error "またはuvをインストールしてください: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

section "インストール実行"

if [ "$INSTALL_METHOD" = "pypi" ]; then
    info "PyPIからagents-docs-syncをインストール中..."
    if [ "$PIP_CMD" = "uv pip" ]; then
        uv pip install agents-docs-sync
    else
        $PIP_CMD install agents-docs-sync
    fi
elif [ "$INSTALL_METHOD" = "github" ]; then
    info "GitHubから開発版をインストール中..."
    GITHUB_REPO="https://github.com/your-username/agents-docs-sync.git"
    warn "GitHubリポジトリのURLを設定してください（現在はプレースホルダーです）"

    # 一時ディレクトリにクローン
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

    if command -v git &> /dev/null; then
        info "リポジトリをクローン中..."
        git clone "$GITHUB_REPO" "$TEMP_DIR" || {
            error "リポジトリのクローンに失敗しました"
            exit 1
        }

        info "開発版をインストール中..."
        cd "$TEMP_DIR"
        if [ "$PIP_CMD" = "uv pip" ]; then
            uv pip install -e .
        else
            $PIP_CMD install -e .
        fi
    else
        error "gitが見つかりません。GitHubからインストールするにはgitが必要です"
        exit 1
    fi
fi

section "インストール確認"

# インストール確認
if command -v agents-docs-sync &> /dev/null; then
    INSTALLED_VERSION=$(agents-docs-sync --version 2>&1 || echo "unknown")
    info "インストールが完了しました！"
    info "バージョン: $INSTALLED_VERSION"
    echo ""
    info "使用方法:"
    echo "  agents-docs-sync                    # ドキュメントを生成"
    echo "  agents-docs-sync --detect-only      # 言語検出のみ"
    echo "  agents-docs-sync --help             # ヘルプを表示"
    echo ""
    info "詳細は README.md を参照してください"
else
    warn "agents-docs-syncコマンドが見つかりません"
    warn "PATHを確認してください"
    exit 1
fi

