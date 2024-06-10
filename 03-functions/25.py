def some_func(one: int, two: int, /, three: int, *, four: int) -> None:
    print(one, two, three, four)


some_func(1, 2, 3, four=4)
some_func(1, 2, three=3, four=4)
some_func(1, 2, 3, 4)  # type: ignore[misc]
