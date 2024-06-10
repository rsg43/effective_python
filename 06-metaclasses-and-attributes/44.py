class Test:

    def __init__(self) -> None:
        self._a = 10
        self._b: int

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, value: int) -> None:
        if value < 0:
            raise ValueError("Value must be greater than 0")
        self._a = value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        if hasattr(self, "_b"):
            raise AttributeError("Attribute can only be set once")
        self._b = value


t = Test()
print(t.a)
t.a = 20

try:
    t.a = -10
except ValueError as e:
    print(e)

try:
    print(t.b)
except AttributeError as e:
    print(e)

t.b = 30
print(t.b)

try:
    t.b = 40
except AttributeError as e:
    print(e)
