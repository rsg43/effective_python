from typing import TypeVar, Generic
from weakref import WeakKeyDictionary

T = TypeVar("T")


class Grade(int, Generic[T]):

    def __init__(self) -> None:
        self._value: WeakKeyDictionary[T, int] = WeakKeyDictionary()

    def __get__(self, instance: T, owner: type[T]) -> int:
        _ = owner
        if instance is None:
            return self
        val = self._value.get(instance, 0)
        return val

    def __set__(self, instance: T, value: int) -> None:
        if not (0 <= value <= 100):
            raise ValueError("Grade must be between 0 and 100")
        self._value[instance] = value


class Exam:

    def __init__(self) -> None:
        self.math: Grade[Exam] = Grade()
        self.science: Grade[Exam] = Grade()
        self.history: Grade[Exam] = Grade()


first_exam = Exam()
first_exam.math = 90
first_exam.science = 80
try:
    first_exam.history = 1000
except ValueError as e:
    print(e)
    first_exam.history = 100

print(first_exam.math)
print(first_exam.science)
print(first_exam.history)

second_exam = Exam()
second_exam.math = 70
second_exam.science = 60
second_exam.history = 50

print(first_exam.math)
print(first_exam.science)
print(first_exam.history)
print(second_exam.math)
print(second_exam.science)
print(second_exam.history)
