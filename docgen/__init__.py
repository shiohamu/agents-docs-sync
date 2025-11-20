"""
汎用ドキュメント自動生成システム

GitHubにプッシュされた変更をトリガーに、テスト実行・ドキュメント生成・AGENTS.mdの自動更新を行うパイプライン
"""

__version__ = "0.0.1"

from .config_manager import ConfigManager
from .docgen import DocGen, main
from .document_generator import DocumentGenerator
from .generator_factory import GeneratorFactory
from .language_detector import LanguageDetector

__all__ = [
    "DocGen",
    "main",
    "ConfigManager",
    "LanguageDetector",
    "DocumentGenerator",
    "GeneratorFactory",
]
