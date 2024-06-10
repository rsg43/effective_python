from typing import Iterator


def iter_1() -> Iterator[str]:
    yield "Starting to iterate..."
    for i in range(10):
        yield str(i)
    yield "Done iterating."


iter_2 = (value.upper() for value in iter_1())
print(iter_2)
print(list(iter_2))
