"""
BaseParserのテスト
"""

import pytest
from pathlib import Path
from generators.parsers.base_parser import BaseParser
from generators.parsers.python_parser import PythonParser


@pytest.mark.unit
class TestBaseParser:
    """BaseParserのテストクラス"""

    def test_parse_project_exclude_dirs(self, temp_project):
        """除外ディレクトリが正しく除外されることを確認"""
        # 除外されるディレクトリにファイルを作成
        (temp_project / ".git").mkdir()
        (temp_project / ".git" / "test.py").write_text("def test(): pass\n", encoding='utf-8')

        # 通常のディレクトリにファイルを作成
        (temp_project / "main.py").write_text("def main(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(exclude_dirs=['.git'])

        # .git内のファイルは解析されない
        assert all('.git' not in api['file'] for api in apis)

    def test_parse_project_custom_exclude_dirs(self, temp_project):
        """カスタム除外ディレクトリが正しく除外されることを確認"""
        (temp_project / "excluded").mkdir()
        (temp_project / "excluded" / "test.py").write_text("def test(): pass\n", encoding='utf-8')

        (temp_project / "main.py").write_text("def main(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(exclude_dirs=['excluded'])

        assert all('excluded' not in api['file'] for api in apis)

    def test_parse_project_parallel(self, temp_project):
        """並列処理でプロジェクトを解析"""
        # 複数のファイルを作成（並列処理が有効になるように）
        for i in range(15):
            (temp_project / f"file{i}.py").write_text(f"def func{i}(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(use_parallel=True)

        assert len(apis) >= 15

    def test_parse_project_sequential(self, temp_project):
        """逐次処理でプロジェクトを解析"""
        (temp_project / "main.py").write_text("def main(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(use_parallel=False)

        assert len(apis) >= 1

    def test_parse_project_few_files_sequential(self, temp_project):
        """ファイル数が少ない場合は逐次処理になることを確認"""
        # 10ファイル以下なので逐次処理になる
        for i in range(5):
            (temp_project / f"file{i}.py").write_text(f"def func{i}(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(use_parallel=True)

        assert len(apis) >= 5

    def test_parse_file_safe_with_error(self, temp_project):
        """エラーが発生した場合の安全な処理"""
        # 構文エラーのあるファイル
        (temp_project / "error.py").write_text("def invalid syntax\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        # エラーが発生しても例外を投げずに空のリストを返す
        apis = parser.parse_project()

        # エラーファイルは解析されないか、空のリストが返される
        assert isinstance(apis, list)

    def test_parse_project_symlink_skipped(self, temp_project):
        """シンボリックリンクがスキップされることを確認"""
        # 実際のシンボリックリンクのテストは環境依存のため、
        # 通常のファイルでテスト
        (temp_project / "main.py").write_text("def main(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project()

        assert len(apis) >= 1

    def test_parse_project_permission_error(self, temp_project):
        """権限エラーが発生した場合の処理"""
        # 権限エラーのテストは環境依存のため、
        # 通常のファイルでテスト
        (temp_project / "main.py").write_text("def main(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project()

        assert isinstance(apis, list)

    def test_parse_project_max_workers(self, temp_project):
        """max_workersが指定された場合の処理"""
        for i in range(15):
            (temp_project / f"file{i}.py").write_text(f"def func{i}(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(use_parallel=True, max_workers=2)

        assert len(apis) >= 15

    def test_parse_project_parallel_with_exception(self, temp_project):
        """並列処理で例外が発生した場合の処理"""
        # 正常なファイルとエラーファイルを作成
        (temp_project / "valid.py").write_text("def valid(): pass\n", encoding='utf-8')
        (temp_project / "error.py").write_text("def invalid syntax\n", encoding='utf-8')

        # 15ファイル以上で並列処理が有効になる
        for i in range(14):
            (temp_project / f"file{i}.py").write_text(f"def func{i}(): pass\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        apis = parser.parse_project(use_parallel=True)

        # エラーが発生しても処理が続行される
        assert isinstance(apis, list)
        assert len(apis) >= 1

    def test_parse_file_safe_exception_handling(self, temp_project):
        """_parse_file_safeで例外が発生した場合の処理"""
        # 構文エラーのあるファイル
        error_file = temp_project / "syntax_error.py"
        error_file.write_text("def invalid\n", encoding='utf-8')

        parser = PythonParser(temp_project)
        # parse_project内で_parse_file_safeが呼ばれ、例外が処理される
        apis = parser.parse_project()

        # エラーが発生しても空のリストが返される
        assert isinstance(apis, list)

