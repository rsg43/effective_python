from typing import Iterator


def greet_iter() -> Iterator[str]:
    yield "Hello, welcome to this demo"
    yield "I hope you enjoy it."


def func_iter() -> Iterator[str]:
    yield "Starting to iterate..."
    for i in range(10):
        yield str(i)
    yield "Done iterating."


def finish_iter() -> Iterator[str]:
    yield "Goodbye, thanks for joining us."


def full_iter() -> Iterator[str]:
    yield from greet_iter()
    yield from func_iter()
    yield from finish_iter()


for value in full_iter():
    print(value)
