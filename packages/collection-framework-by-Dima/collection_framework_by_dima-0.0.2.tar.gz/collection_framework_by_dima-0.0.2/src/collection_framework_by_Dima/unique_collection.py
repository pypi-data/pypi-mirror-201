from collections import Counter
from functools import lru_cache

from .my_exceptions import UniqueTypeError


@lru_cache(maxsize=None)
def unique_symbol(line: str) -> int:
    if not isinstance(line, str):
        raise UniqueTypeError('Type does not match')
    return list(Counter(line).values()).count(1)


def unique_symbol_in_list(line: list) -> list:
    if not isinstance(line, list):
        raise UniqueTypeError('Data type must be list')
    return list(map(unique_symbol, line))
