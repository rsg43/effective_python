from typing import Callable, Iterator


def get_iter() -> Iterator[int]:
    for i in range(10):
        yield i


def find_average(func: Callable[[], Iterator[int]]) -> float:
    count = len(list(func()))
    total = sum(func())
    return total / count


res = find_average(get_iter)
print(res)


class TestIter:
    def __init__(self) -> None:
        self._size = 10

    def __iter__(self) -> Iterator[int]:
        for i in range(self._size):
            yield i


def find_average_defensive(func: TestIter) -> float:
    count = len(list(func))
    total = sum(func)
    return total / count


res = find_average_defensive(TestIter())
print(res)

test = TestIter()
for i in test:
    print(i)
