"""
汎用ドキュメント自動生成システム

GitHubにプッシュされた変更をトリガーに、テスト実行・ドキュメント生成・AGENTS.mdの自動更新を行うパイプライン
"""

__version__ = "0.0.1"

from .docgen import DocGen, main

__all__ = ["DocGen", "main"]
