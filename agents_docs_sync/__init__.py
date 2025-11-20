"""
agents-docs-sync パッケージ

このパッケージは、GitHubにプッシュされた変更をトリガーに、
テスト実行・ドキュメント生成・AGENTS.mdの自動更新を行うパイプラインです。

パッケージ名とモジュール名を一致させるためのラッパーモジュールです。
実際の実装は`docgen`パッケージにあります。
"""

__version__ = "0.0.5"

# docgenモジュールを再エクスポート
from docgen import DocGen, main

__all__ = ["DocGen", "main"]
