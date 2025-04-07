from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES, wraps
from inspect import BoundArguments, signature
from typing import Any, Callable, Iterable, Literal

from pipe_fp import pipe


def mask[**P](
    wrapped: Callable[P, Any],
    assigned: Iterable[
        Literal[
            "__module__",
            "__name__",
            "__qualname__",
            "__doc__",
            "__annotations__",
            "__type_params__",
        ]
    ] = WRAPPER_ASSIGNMENTS,
    updated: Iterable[Literal["__dict__"]] = WRAPPER_UPDATES,
):
    """
    mask docstring 📄
    """

    def outer_wrapper[R](f: Callable[..., R]) -> Callable[P, R]:
        @wraps(wrapped, assigned, updated)
        def inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            def bind_partial(f: Callable[P, Any]):
                return signature(f).bind_partial(*args, **kwargs)

            def apply_defaults(ba: BoundArguments):
                return ba.apply_defaults() or ba

            def callback(ba: BoundArguments):
                return f(*ba.args, **ba.kwargs)

            return pipe(bind_partial, apply_defaults, callback)(wrapped)

        return inner_wrapper

    return outer_wrapper
