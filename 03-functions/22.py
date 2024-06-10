def rounding(places: int, *numbers: float) -> list[str]:
    return [f"{number:.{places}f}" for number in numbers]


print(rounding(2, 3.14159265359, 2.71828182846, 1.61803398875))
