from inspect import Signature


def merge_annotations(wrapped: Signature, wrapper: Signature) -> Signature:
    return wrapped.replace(return_annotation=wrapper.return_annotation)
