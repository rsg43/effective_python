class Test:

    def __init__(self) -> None:
        self._value: int
        self._count = 0

    @property
    def value(self) -> int:
        if not hasattr(self, "_value"):
            self._value = 0
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        if value == 0:
            print("Resetting value and count to 0")
            self._count = 0
        elif value < 0:
            raise ValueError("Value must be greater than 0")
        self._value = value

    def plus(self) -> None:
        self._count += self._value

    def __repr__(self) -> str:
        return f"Value: {self.value}, Count: {self._count}"


test = Test()
print(test)
test.value = 10
test.plus()
test.plus()
print(test)
test.value = 0
print(test)
