import inspect
from string import Formatter
from collections import ChainMap
from typing import List

class EnrichedException(Exception):
    def __init__(self, cause: Exception):
        super().__init__(cause)
        self.cause = cause
        self.stack = []

    def __str__(self) -> str:
        output = self.stack[-1] + "\n"
        level = 0

        for level, msg in enumerate(self.stack[-2::-1]):
            output += (" " * level) + "↳ " + msg + "\n"

        output += (" " * (level+1)) + "↳ " + str(self.cause)
        return output

class InvalidEnrichDecoratorUsage(Exception):
    pass

def fmt(template: str):
    # filter out None (no more format fields found) but not empty strings (positional format field)
    template_fields = [fname for _, fname, _, _ in Formatter().parse(template) if fname is not None]
    if any(map(lambda s: s is not None and len(s) == 0 , template_fields)):
        raise InvalidEnrichDecoratorUsage(
            f"Template contains positional format placeholders. "
            f"This is not allowed: '{template}'"
        )

    def _inner(fn):
        spec = inspect.signature(fn)
        # validate that all args are actually part of the function signature

        for field in template_fields:
            if field not in spec.parameters:
                raise InvalidEnrichDecoratorUsage(
                    f"template field {field} not in fn signature: {fn.__qualname__}"
                )

        def _handler(*call_args, **call_kwargs):
            try:
                return fn(*call_args, **call_kwargs)
            except Exception as ex:
                bound = spec.bind(*call_args, **call_kwargs)
                bound.apply_defaults()

                if not isinstance(ex, EnrichedException):
                    ex = EnrichedException(ex)

                # the k can either be in args or kwargs
                lookup = ChainMap(bound.arguments, bound.kwargs)

                msg = Formatter().vformat(template, [], lookup)
                ex.stack.append(msg)

                # re-raise otherwise it is
                # "during handling of exception .. another one occured"
                raise ex from ex

        return _handler
    return _inner


def with_args(*args: List[str]):
    def _inner(fn):
        spec = inspect.signature(fn)
        # validate that all args are actually part of the function signature
        for arg in args:
            if arg not in spec.parameters:
                raise InvalidEnrichDecoratorUsage(
                    f"arg {arg} not in fn signature: {fn.__qualname__}"
                )

        def _handler(*call_args, **call_kwargs):
            try:
                return fn(*call_args, **call_kwargs)
            except Exception as ex:
                bound = spec.bind(*call_args, *call_kwargs)
                bound.apply_defaults()

                if not isinstance(ex, EnrichedException):
                    ex = EnrichedException(ex)

                # the k can either be in args or kwargs
                lookup = ChainMap(bound.arguments, bound.kwargs)

                kvs = [f"{arg} = {lookup[arg]}" for arg in (args or spec.parameters.keys())]
                msg = f"during call of {fn.__qualname__}({', '.join(kvs)})"
                ex.stack.append(msg)

                # re-raise otherwise it is
                # "during handling of exception .. another one occured"
                raise ex from ex

        return _handler
    return _inner

def with_fn_name():
    def _inner(fn):
        def _handler(*call_args, **call_kwargs):
            try:
                return fn(*call_args, **call_kwargs)
            except Exception as ex:
                if not isinstance(ex, EnrichedException):
                    ex = EnrichedException(ex)

                ex.stack.append(f"during call of {fn.__qualname__}")

                # re-raise otherwise it is
                # "during handling of exception .. another one occured"
                raise ex from ex

        return _handler
    return _inner
