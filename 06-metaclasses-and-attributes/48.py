from typing import Any


class Meta(type):
    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]
    ) -> type:
        print("Meta.__new__ called")
        print(f"cls: {cls}\nname: {name}\nbases: {bases}\ndct: {dct}")
        return super().__new__(cls, name, bases, dct)


class MyClass(metaclass=Meta):
    pass


class MySubclass(MyClass):
    pass


subclass = MySubclass()


class ValidatePolygon(type):
    def __new__(
        cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]
    ) -> type:
        # Don't validate the abstract Polygon class
        if bases:
            if dct["sides"] < 3:
                raise ValueError("Polygons need 3+ sides")
        return super().__new__(cls, name, bases, dct)


class Polygon(metaclass=ValidatePolygon):
    sides: int

    @classmethod
    def interior_angles(cls) -> int:
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


try:

    class Line(Polygon):
        sides = 2

except ValueError as e:
    print(e)


class BetterPolygon:
    sides: int

    def __init_subclass__(cls) -> None:
        if cls.sides < 3:
            raise ValueError("Polygons need 3+ sides")

    @classmethod
    def interior_angles(cls) -> int:
        return (cls.sides - 2) * 180


class Hexagon(BetterPolygon):
    sides = 6


try:

    class Point(BetterPolygon):
        sides = 1

except ValueError as e:
    print(e)


class Quadrilateral(BetterPolygon):
    sides = 4
    side_lengths: tuple[float, float, float, float]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if len(cls.side_lengths) != cls.sides:
            raise ValueError("Quadrilaterals need 4 sides")


class Square(Quadrilateral):
    side_lengths = (1, 1, 1, 1)


try:

    class NewTriangle(Quadrilateral):
        side_lengths = (1, 1, 1)  # type: ignore[assignment]

except ValueError as e:
    print(e)

try:

    class NewPoint(Quadrilateral):
        sides = 1
        side_lengths = tuple()  # type: ignore[assignment]

except ValueError as e:
    print(e)
