from collections.abc import Sequence
from typing import TypeVar, overload, Self, Any

T = TypeVar("T")


class BadType(Sequence[T]):
    pass


try:
    seq_bad = BadType()  # type: ignore[abstract, var-annotated]
except TypeError as e:
    print(e)


class GoodType(Sequence[T]):

    def __init__(self, items: list[T]):
        self.items = items
        self.items_copy = items.copy()

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, sl: slice) -> Self: ...

    def __getitem__(self, value: Any) -> Any:
        if isinstance(value, int):
            return self.items[value]
        elif isinstance(value, slice):
            sl_list = self.items[value]
            if isinstance(sl_list, list):
                return GoodType(sl_list)
            else:
                raise ValueError("Slice is not a list")
        else:
            raise ValueError("Value is not an int or slice")

    def __len__(self) -> int:
        return len(self.items)

    def recreate(self) -> None:
        self.items = self.items_copy.copy()

    def pop(self, index: int) -> T:
        return self.items.pop(index)


seq = GoodType([1, 2, 3])
print(seq[0])
print(len(seq))
seq.pop(0)
print(len(seq))
seq.recreate()
print(len(seq))


seq2 = GoodType(["1", "2", "3"])
print(seq2[0])
print(len(seq2))
print(seq2[0:2])
print(seq2[0:2].items)
