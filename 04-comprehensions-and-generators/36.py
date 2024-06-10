from typing import Iterator
from itertools import (
    chain,
    repeat,
    cycle,
    tee,
    zip_longest,
    islice,
    takewhile,
    dropwhile,
    filterfalse,
    accumulate,
    product,
    permutations,
    combinations,
    combinations_with_replacement,
)


def iter_1() -> Iterator[int]:
    for i in range(5):
        yield i


def iter_2() -> Iterator[int]:
    for i in range(5, 11):
        yield i


for i in chain(iter_1(), iter_2()):
    print(i)

for i in repeat(1, 10):
    print(i)

cycle_iter = cycle(iter_1())
for i in range(10):
    print(next(cycle_iter))

iter_1_a, iter_1_b = tee(iter_1(), 2)
for i, j in zip(iter_1_a, iter_1_b):
    print(i, j)

for i, j in zip_longest(iter_1(), iter_2()):
    print(i, j)

for i in islice(iter_1(), 0, 5, 2):
    print(i)

for i in takewhile(lambda x: x < 2, iter_1()):
    print(i)

for i in dropwhile(lambda x: x < 3, iter_1()):
    print(i)

for i in filterfalse(lambda x: x < 3, iter_1()):
    print(i)

for i in accumulate(iter_1()):
    print(i)

for i in accumulate(iter_1(), lambda x, y: (x + y) % 2):
    print(i)

for i, j in product(iter_1(), iter_2()):
    print(i, j)

for i, j in permutations(iter_1(), 2):
    print(i)

for i, j in combinations(iter_1(), 2):
    print(i)

for i, j in combinations_with_replacement(iter_1(), 2):
    print(i)
