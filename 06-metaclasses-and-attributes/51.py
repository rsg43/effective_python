from functools import wraps
from typing import Any, Callable
import types


def trace_func(func: Callable[..., Any]) -> Callable[..., Any]:
    if hasattr(func, "tracing"):
        return func

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")

    wrapper.tracing = True  # type: ignore[attr-defined]
    return wrapper


class TraceDict(dict[Any, Any]):

    @trace_func
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)

    @trace_func
    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)

    @trace_func
    def __delitem__(self, key: Any) -> None:
        super().__delitem__(key)


trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType,
)


def trace(debug: bool = False) -> Callable[[object], object]:
    def dec_trace(cls: object) -> object:
        for key in dir(cls):
            value = getattr(cls, key)
            if isinstance(value, trace_types):
                setattr(cls, key, trace_func(value))
                if debug:
                    print(f"Patched: {key}")
            elif debug:
                print(f"Ignored: {key}")
                print(type(value))
        return cls

    return dec_trace


@trace()
class BetterTraceDict(dict[Any, Any]):
    pass


def test_dict(td: Any) -> None:
    td["x"] = 1
    td["y"] = 2

    td["x"]
    del td["y"]
    try:
        print(td["y"])
    except KeyError:
        pass


print("Bad:")
test_dict(TraceDict())
print("Good:")
test_dict(BetterTraceDict())

print("Debug:")


@trace(debug=True)
class DebugTraceDict(dict[Any, Any]):
    pass


btd = DebugTraceDict()
btd.__setitem__("x", 1)
