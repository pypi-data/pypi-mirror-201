from argparse import Namespace
from unittest.mock import mock_open, patch

import pytest

from collection_framework import NoArgumentsError, get_result


@patch('collection_framework.collect_framework.unique_symbol')
@patch('collection_framework.collect_framework.argparse.ArgumentParser.parse_args')
def test_string(mock, mock_unique_symbol):
    mock.return_value = Namespace(file=None, string='assdqrt')
    mock_unique_symbol.return_value = 5
    assert get_result() == 5
    mock_unique_symbol.assert_called_once_with('assdqrt')


@patch('collection_framework.collect_framework.unique_symbol')
@patch('collection_framework.collect_framework.argparse.ArgumentParser.parse_args')
@patch('tests.test_collect_framework.open', mock_open(read_data='asdas\nas'))
def test_file(mock, mock_unique_symbol):
    mock.return_value = Namespace(file=open(), string=None)
    mock_unique_symbol.return_value = 2
    assert get_result() == 2
    mock_unique_symbol.assert_called_once_with('asdas\nas')


@patch('collection_framework.collect_framework.unique_symbol')
@patch('collection_framework.collect_framework.argparse.ArgumentParser.parse_args')
@patch('tests.test_collect_framework.open', mock_open(read_data='asdas\nas'))
def test_file_priority(mock, mock_unique_symbol):
    mock.return_value = Namespace(file=open(), string='qwerasdasd')
    mock_unique_symbol.return_value = 2
    assert get_result() == 2
    mock_unique_symbol.assert_called_once_with('asdas\nas')


@patch('collection_framework.collect_framework.argparse.ArgumentParser.parse_args')
def test_exeption(mock):
    mock.return_value = Namespace(file=None, string=None)
    with pytest.raises(NoArgumentsError) as excinfo:
        get_result()
    assert str(excinfo.value) == 'You need to enter arguments'
