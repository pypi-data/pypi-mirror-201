from collections import Counter
from functools import cache

from .exceptions import UniqueTypeError


@cache
def __unique_count(text: str) -> int:
    return tuple(Counter(text).values()).count(1)


def unique_symbol(text: str) -> int:
    if not isinstance(text, unique_symbol.__annotations__["text"]):
        raise UniqueTypeError(f"'text' must be {unique_symbol.__annotations__['text']}")
    return __unique_count(text)


def unique_symbol_in_list(strings: list) -> list[int]:
    if not isinstance(strings, unique_symbol_in_list.__annotations__["strings"]):
        raise UniqueTypeError(
            f"'strings' must be {unique_symbol_in_list.__annotations__['strings']}"
        )
    return list(map(unique_symbol, strings))
