from typing import Generator, Iterator, Union


def iter_1() -> Generator[float, Union[None, float], None]:
    multiplier = 0.0
    for i in range(10):
        new_multiplier = yield i * multiplier
        if new_multiplier is not None:
            multiplier = new_multiplier


iterator = iter_1()
iterator.send(None)
iterator.send(2)

for i in iterator:
    if i >= 10:
        iterator.send(0.5)
    print(i)


def base_iter() -> Iterator[int]:
    for i in range(10):
        yield i


def multiplier_iter(base: Iterator[int]) -> Iterator[int]:
    multiplier = 0
    for i in range(10):
        multiplier = next(base)
        yield i * multiplier


for i in multiplier_iter(base_iter()):
    print(i)
