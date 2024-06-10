class Base:
    def __init__(self, value: float) -> None:
        self.value = value


class Double:
    value: float

    def __init__(self) -> None:
        self.value *= 2


class Square:
    value: float

    def __init__(self) -> None:
        self.value **= 2


class Inherit(Base, Double, Square):
    def __init__(self, value: float) -> None:
        Base.__init__(self, value)
        Double.__init__(self)
        Square.__init__(self)


class InheritReverse(Base, Double, Square):
    def __init__(self, value: float) -> None:
        Base.__init__(self, value)
        Square.__init__(self)
        Double.__init__(self)


print(Inherit(3).value)
print(InheritReverse(3).value)


class DoubleInherit(Base):
    def __init__(self, value: float) -> None:
        Base.__init__(self, value)
        self.value *= 2


class SquareInherit(Base):
    def __init__(self, value: float) -> None:
        Base.__init__(self, value)
        self.value **= 2


class InheritInherit(DoubleInherit, SquareInherit):
    def __init__(self, value: float) -> None:
        DoubleInherit.__init__(self, value)
        SquareInherit.__init__(self, value)


print(InheritInherit(3).value)


class DoubleInheritSuper(Base):
    def __init__(self, value: float) -> None:
        super().__init__(value)
        self.value *= 2


class SquareInheritSuper(Base):
    def __init__(self, value: float) -> None:
        super().__init__(value)
        self.value **= 2


class InheritInheritSuper(DoubleInheritSuper, SquareInheritSuper):
    def __init__(self, value: float) -> None:
        super().__init__(value)


print(InheritInheritSuper(3).value)
print(InheritInheritSuper.mro())
