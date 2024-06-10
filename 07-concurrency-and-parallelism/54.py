from threading import Thread, Lock


class Counter:

    def __init__(self) -> None:
        self.value = 0

    def increment(self, val: int) -> None:
        count = getattr(self, "value")
        result = count + val
        setattr(counter, "value", result)


def worker(index: int, number: int, counter: Counter) -> None:
    for _ in range(number):
        _ = index
        counter.increment(1)


counter = Counter()
threads: list[Thread] = []
for i in range(5):
    thread = Thread(target=worker, args=(i, 100000, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Expected: {5 * 100000}, Got: {counter.value}")


class LockingCounter:
    def __init__(self) -> None:
        self.value = 0
        self.lock = Lock()

    def increment(self, val: int) -> None:
        with self.lock:
            count = getattr(self, "value")
            result = count + val
            setattr(counter, "value", result)


locking_counter = LockingCounter()
locking_threads: list[Thread] = []
for i in range(5):
    locking_thread = Thread(target=worker, args=(i, 100000, locking_counter))
    locking_threads.append(thread)
    locking_thread.start()

for locking_thread in locking_threads:
    locking_thread.join()

print(f"Expected: {5 * 100000}, Got: {locking_counter.value}")
