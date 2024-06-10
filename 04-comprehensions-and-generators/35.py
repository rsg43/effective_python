from typing import Generator, Optional


class MyExc(Exception):
    pass


class Timer:
    def __init__(self) -> None:
        self.count = 0
        self.running = True
        self._iter: Optional[Generator[int, None, None]] = None

    def __iter__(self) -> Generator[int, None, None]:
        while self.running:
            try:
                yield self.count
                self.count += 1
            # Below only needed for throw option, complicated
            except MyExc:
                print("Caught exception")
                self.running = False
                break

    def __next__(self) -> int:
        if self._iter is None:
            self._iter = self.__iter__()
        return next(self._iter)

    def throw(self, exc: Exception) -> None:
        if self._iter is None:
            self._iter = self.__iter__()
        self._iter.throw(exc)


timer = Timer()

for i in timer:
    print(i)
    if i >= 10:
        timer.running = False


def run() -> None:
    timer = Timer()

    current = 0
    while True:
        try:
            if current >= 10:
                timer.throw(MyExc("Uh oh!"))
            else:
                current = next(timer)
        except StopIteration:
            break
        else:
            print(current)


run()
