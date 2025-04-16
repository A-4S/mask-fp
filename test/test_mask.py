from inspect import signature
from typing import Any

from masks_fp import masks

from .library import demo_func


@masks(demo_func, assigned=('__doc__',))
def wrapper(*args, **kwargs) -> tuple[tuple, dict[str, Any]]:
    '''
    From ``wrapper`` ``docstring``. 👋
    '''
    return args, kwargs


def test_mask():
    # check return values
    assert wrapper(1) == ((1, 2), {'c': 3})
    assert wrapper(1, 2) == ((1, 2), {'c': 3})
    assert wrapper(1, 2, c=3) == ((1, 2), {'c': 3})
    assert wrapper(1, c=3, b=2) == ((1, 2), {'c': 3})

    # check return annotations
    assert wrapper.__annotations__['return'] == tuple[tuple, dict[str, Any]]
    assert signature(wrapper).return_annotation == tuple[tuple, dict[str, Any]]

    # ensure successful wraps call
    assert wrapper.__doc__ == demo_func.__doc__
    assert wrapper.__name__ != demo_func.__name__

    # ensure updated signature
    assert signature(wrapper) != signature(demo_func)
