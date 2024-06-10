from collections import defaultdict
from typing import TypeVar


T = TypeVar("T")

scenes = defaultdict(list)

scenes["1"].append("In the first scene")
scenes["2"].append("In the second scene")
scenes["3"].append("In the third scene")
scenes["1"].append("In the opening scene")

print(scenes)


def first(_list: list[T]) -> T:
    return _list[0]
