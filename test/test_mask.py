from mask_fp import mask

from .library import demo_func


@mask(demo_func)
def wrapper(*args, **kwargs):
    return args, kwargs


def test_mask():
    assert wrapper(1) == ((1, 2), {'c': 3})
    assert wrapper(1, 2) == ((1, 2), {'c': 3})
    assert wrapper(1, 2, c=3) == ((1, 2), {'c': 3})
    assert wrapper(1, c=3, b=2) == ((1, 2), {'c': 3})
