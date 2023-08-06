import inspect

import pytest

from collection_framework.unique_collection import (UniqueTypeError,
                                                    unique_symbol,
                                                    unique_symbol_in_list)


@pytest.mark.parametrize('test_input', [1, 1.1, {'qe': 'eq'}])
def test_type_one(test_input):
    with pytest.raises(UniqueTypeError):
        inspect.unwrap(unique_symbol)(test_input)


@pytest.mark.parametrize('test_input, expected', [('abbbccdf', 3),
                                                  ('adfgfadd', 1), ('', 0),
                                                  ('asdfghj', 7)])
def test_unique_symbol_one(test_input, expected):
    assert unique_symbol(test_input) == expected


@pytest.mark.parametrize('test_input, expected', [(['abc123'], [6]),
                                                  (['aaabbbccc123'], [3]),
                                                  ([''], [0])])
def test_unique_symbol_in_list(test_input, expected):
    assert unique_symbol_in_list(test_input) == expected


@pytest.mark.parametrize('test_input', [1, 1.1, {'qe': 'fa'}])
def test_type_in_list(test_input):
    with pytest.raises(UniqueTypeError):
        unique_symbol_in_list(test_input)
