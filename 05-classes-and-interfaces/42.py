class Test:
    def __init__(self) -> None:
        self.__x = 42
        self._y = 21
        self.z = 10

    def get_private(self) -> int:
        return self.__x


t = Test()
assert not hasattr(t, "__x")
assert t.get_private() == 42
assert t._Test__x == 42  # type: ignore[attr-defined]

assert t._y == 21
assert t.z == 10
