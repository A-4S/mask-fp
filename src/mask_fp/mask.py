from functools import wraps
from inspect import BoundArguments, signature
from typing import Any, Callable

from pipe_fp import pipe


def mask[**P](f1: Callable[P, Any]):
    def outer_wrapper[R](f2: Callable[..., R]) -> Callable[P, R]:
        @wraps(f1)
        def inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            def bind_partial(f: Callable[P, Any]):
                return signature(f).bind_partial(*args, **kwargs)


            def apply_defaults(ba: BoundArguments):
                return ba.apply_defaults() or ba


            def callback(ba: BoundArguments):
                return f2(*ba.args, **ba.kwargs)


            return pipe(
                bind_partial,
                apply_defaults,
                callback
            )(f1)

        return inner_wrapper

    return outer_wrapper
