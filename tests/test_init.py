"""
docgenパッケージ初期化のテスト
"""

import pytest


def test_version_info():
    """バージョン情報のテスト"""
    import docgen

    assert hasattr(docgen, "__version__")
    assert isinstance(docgen.__version__, str)
    assert len(docgen.__version__) > 0


def test_main_exports():
    """メインエクスポートのテスト"""
    import docgen

    # DocGenクラスのインポート確認
    assert hasattr(docgen, "DocGen")
    from docgen import DocGen

    assert callable(DocGen)

    # main関数のインポート確認
    assert hasattr(docgen, "main")
    from docgen import main

    assert callable(main)


def test_all_exports():
    """__all__エクスポートのテスト"""
    import docgen

    # __all__が存在することを確認
    assert hasattr(docgen, "__all__")
    assert isinstance(docgen.__all__, list)

    # __all__に含まれる項目が実際に存在することを確認
    for item in docgen.__all__:
        assert hasattr(docgen, item), f"{item} is in __all__ but not defined"

    # 主要なエクスポートが__all__に含まれていることを確認
    assert "DocGen" in docgen.__all__
    assert "main" in docgen.__all__


def test_package_import():
    """パッケージ全体のインポートテスト"""
    # 正常にインポートできることを確認
    import docgen

    assert docgen is not None

    # サブモジュールのインポートも可能
    import docgen.docgen

    assert docgen.docgen is not None

    import docgen.utils.logger

    assert docgen.utils.logger is not None


def test_docstring():
    """パッケージのdocstringテスト"""
    import docgen

    # docstringが存在することを確認
    assert docgen.__doc__ is not None
    assert len(docgen.__doc__) > 0

    # docstringに主要なキーワードが含まれていることを確認
    docstring = docgen.__doc__.lower()
    assert "ドキュメント" in docstring or "document" in docstring
    assert "自動生成" in docstring or "auto" in docstring
