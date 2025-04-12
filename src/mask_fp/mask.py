from collections.abc import Callable
from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES, wraps
from inspect import BoundArguments, Signature, signature
from typing import Any, Iterable, Literal

from pipe_fp import pipe

from .library import merge_annotations, set_return_annotations
from .type.types import P, T


def mask(
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

    def outer_wrapper(wrapper: Callable[..., T]) -> Callable[P, T]:
        @wraps(wrapped, assigned, updated)
        def inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            def bind_partial(s: Signature):
                return s.bind_partial(*args, **kwargs)

            def apply_defaults(ba: BoundArguments):
                return ba.apply_defaults() or ba

            def callback(ba: BoundArguments):
                return wrapper(*ba.args, **ba.kwargs)

            return pipe(signature, bind_partial, apply_defaults, callback)(wrapped)

        return pipe[tuple[Callable, Callable]](
            lambda fs: [signature(f) for f in fs],
            lambda signatures: merge_annotations(*signatures),
            lambda merged_s: set_return_annotations(inner_wrapper, merged_s),
        )((wrapped, wrapper)) or inner_wrapper

    return outer_wrapper
