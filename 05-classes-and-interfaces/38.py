def filter_events(numbers: list[int]) -> list[int]:

    def is_even(n: int) -> bool:
        return n % 2 == 0

    return list(filter(is_even, numbers))


scenes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(filter_events(scenes))


class EventFilter:
    def __init__(self) -> None:
        self.is_even = lambda n: n % 2 == 0

    def __call__(self, numbers: list[int]) -> list[int]:
        return list(filter(self.is_even, numbers))


filter_events_class = EventFilter()
print(filter_events_class(scenes))
