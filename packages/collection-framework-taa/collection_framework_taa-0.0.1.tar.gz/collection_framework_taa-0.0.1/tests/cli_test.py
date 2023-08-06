import io
from argparse import Namespace
from unittest.mock import patch

import pytest

from collection_framework.cli import get_result
from collection_framework.exceptions import UniqueArgsError

STRING_TEXT = "abcd"
FILE_TEXT = "abcdefg\nhi"


@patch("collection_framework.cli.ArgumentParser.parse_args")
@patch("collection_framework.cli.unique_symbol")
class TestCLI():

    def test_exception(self, _, parse_args_mock):
        with pytest.raises(UniqueArgsError) as excinfo:
            parse_args_mock.return_value = Namespace(string=None, file=None)
            get_result()
        assert excinfo.value.args[0] == "No arguments"

    def test_string(self, unique_symbol_mock, parse_args_mock):
        parse_args_mock.return_value = Namespace(string=STRING_TEXT, file=None)
        unique_symbol_mock.return_value = 4
        assert get_result() == 4
        unique_symbol_mock.assert_called_once_with(STRING_TEXT)

    def test_file(self, unique_symbol_mock, parse_args_mock):
        parse_args_mock.return_value = Namespace(
            string=None, file=io.TextIOWrapper(
                io.BytesIO(FILE_TEXT.encode("utf-8"))
            )
        )
        unique_symbol_mock.return_value = 10
        assert get_result() == 10
        unique_symbol_mock.assert_called_once_with(FILE_TEXT)

    def test_both(self, unique_symbol_mock, parse_args_mock):
        parse_args_mock.return_value = Namespace(
            string=STRING_TEXT, file=io.TextIOWrapper(
                io.BytesIO(FILE_TEXT.encode("utf-8"))
            )
        )
        unique_symbol_mock.return_value = 10
        assert get_result() == 10
        unique_symbol_mock.assert_called_once_with(FILE_TEXT)
