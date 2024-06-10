from typing import Callable, Any

from functools import wraps


def trace(func: Callable[[int], int]) -> Callable[[int], int]:
    def wrapper(*args: Any, **kwargs: Any) -> int:
        print(f"Calling {func.__name__} with {args} and {kwargs}")
        original_result = func(*args, **kwargs)
        print(f"{func.__name__} returned {original_result}")
        return original_result

    return wrapper


@trace
def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


fibonacci(5)
print(type(fibonacci))
print(fibonacci)
print(fibonacci.__name__)


def new_trace(func: Callable[[int], int]) -> Callable[[int], int]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        print(f"Calling {func.__name__} with {args} and {kwargs}")
        original_result = func(*args, **kwargs)
        print(f"{func.__name__} returned {original_result}")
        return original_result

    return wrapper


@new_trace
def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


fib(5)
print(type(fib))
print(fib)
print(fib.__name__)
