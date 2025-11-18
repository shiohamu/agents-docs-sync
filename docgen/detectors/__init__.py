"""
言語検出モジュール
"""

from .python_detector import PythonDetector
from .javascript_detector import JavaScriptDetector
from .go_detector import GoDetector
from .generic_detector import GenericDetector

__all__ = [
    'PythonDetector',
    'JavaScriptDetector',
    'GoDetector',
    'GenericDetector'
]

