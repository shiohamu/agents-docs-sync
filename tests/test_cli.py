"""
CLIモジュールのテスト
"""

from unittest.mock import patch

from docgen.docgen import CommandLineInterface


class TestCommandLineInterface:
    """CommandLineInterfaceクラスのテスト"""

    def test_init(self):
        """初期化テスト"""
        cli = CommandLineInterface()
        assert cli.docgen is None

    @patch("docgen.docgen.DocGen")
    def test_run_detect_only(self, mock_docgen_class, tmp_path):
        """言語検出のみ実行テスト"""
        mock_docgen = mock_docgen_class.return_value
        mock_docgen.detect_languages.return_value = ["python"]

        cli = CommandLineInterface()

        with patch("argparse.ArgumentParser.parse_args") as mock_args:
            mock_args.return_value = type(
                "Args",
                (),
                {
                    "command": None,
                    "detect_only": True,
                    "no_api_doc": False,
                    "no_readme": False,
                    "config": None,
                },
            )()

            result = cli.run()
            assert result == 0
            mock_docgen.detect_languages.assert_called_once()
