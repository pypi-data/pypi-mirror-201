import pytest

from collection_framework.collect_framework import (UniqueTypeError,
                                                    unique_symbol,
                                                    unique_symbol_in_list)

data = {
    unique_symbol: {
        "correct": (("abc", 3), ("", 0), ("abbbccdf", 3)),
        "exception": ((1,), (1.5,), (["a", "b", "c"],)),
    },
    unique_symbol_in_list: {
        "correct": (
            (["abc", "difj", "hi"], [3, 4, 2]),
            ([""], [0]),
            (["abbbccdf"], [3]),
        ),
        "exception": (([1],), ([1.5],), ([["a", "b", "c"]],)),
    },
}


def get_data(data, key):
    argvalues = [(f, *params) for f, value in data.items() for params in value[key]]
    return {
        "argvalues": argvalues,
        "ids": [
            f"{v[0].__name__}({v[1].__repr__()})"
            for v in argvalues
        ],
    }


@pytest.mark.parametrize("f,p,r", **get_data(data, "correct"))
def test_correct(f, p, r):
    assert f(p) == r


@pytest.mark.parametrize("f,p", **get_data(data, "exception"))
def test_exception(f, p):
    with pytest.raises(UniqueTypeError):
        f(p)


def test_cache():
    def work_time(data):
        from timeit import timeit

        return timeit(lambda: unique_symbol(data), number=1)

    data = "a" * 1000000
    assert work_time(data) / work_time(data) > 10
