from functools import wraps
from typing import Any, Callable


def mask[**P](f1: Callable[P, Any]):
    def outer_wrapper[R](f2: Callable[..., R]) -> Callable[P, R]:
        @wraps(f1)
        def inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return f2(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper
