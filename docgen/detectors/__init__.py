"""
言語検出モジュール
"""

from .generic_detector import GenericDetector
from .go_detector import GoDetector
from .javascript_detector import JavaScriptDetector
from .python_detector import PythonDetector

__all__ = ["PythonDetector", "JavaScriptDetector", "GoDetector", "GenericDetector"]
