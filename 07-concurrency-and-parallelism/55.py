from collections import deque
from threading import Lock, Thread
from typing import Any, Callable, Iterator
import time
from queue import Queue


class BasicQueue:
    def __init__(self) -> None:
        self.items: deque[Any] = deque()
        self.lock = Lock()

    def put(self, item: Any) -> None:
        with self.lock:
            self.items.append(item)

    def get(self) -> Any:
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(
        self, func: Callable[[Any], Any], in_q: BasicQueue, out_q: BasicQueue
    ) -> None:
        super().__init__()
        self.func = func
        self.in_q = in_q
        self.out_q = out_q
        self.polled_count = 0
        self.work_done = 0

    def run(self) -> None:
        start_time = time.time()
        while time.time() - start_time < 1:
            self.polled_count += 1
            try:
                item = self.in_q.get()
            except IndexError:
                time.sleep(0.01)
            else:
                result = self.func(item)
                self.out_q.put(result)
                self.work_done += 1
        print(f"Worker for {self.func.__name__} Complete!!")


class BetterQueue(Queue[Any]):
    SENTINEL = object()

    def close(self) -> None:
        self.put(self.SENTINEL)

    def __iter__(self) -> Iterator[Any]:
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    break
                yield item
            finally:
                self.task_done()


class BetterWorker(Thread):
    def __init__(
        self, func: Callable[[Any], Any], in_q: BetterQueue, out_q: BetterQueue
    ) -> None:
        super().__init__()
        self.func = func
        self.in_q = in_q
        self.out_q = out_q

    def run(self) -> None:
        for item in self.in_q:
            result = self.func(item)
            self.out_q.put(result)
        print(f"Worker for {self.func.__name__} Complete!!")


def square(n: int) -> int:
    return n * n


def halve(n: int) -> float:
    return n / 2


entry_q = BasicQueue()
intermediate_q = BasicQueue()
exit_q = BasicQueue()

threads = [
    Worker(square, entry_q, intermediate_q),
    Worker(halve, intermediate_q, exit_q),
]

for thread in threads:
    thread.start()

for n in range(10):
    entry_q.put(n)

while len(exit_q.items) < 10:
    time.sleep(0.0001)

for thread in threads:
    thread.join()

print(f"Items in exit_q: {exit_q.items}")
print(f"Items in intermediate_q: {intermediate_q.items}")
print(f"Items in entry_q: {entry_q.items}")
print(f"Polled count: {sum(t.polled_count for t in threads)}")
print(f"Work done: {sum(t.work_done for t in threads)}")


start_q = BetterQueue()
mid_q = BetterQueue()
end_q = BetterQueue()

better_threads = [
    BetterWorker(square, start_q, mid_q),
    BetterWorker(square, start_q, mid_q),
    BetterWorker(square, start_q, mid_q),
    BetterWorker(square, start_q, mid_q),
    BetterWorker(halve, mid_q, end_q),
    BetterWorker(halve, mid_q, end_q),
]

for better_thread in better_threads:
    better_thread.start()

for n in range(10):
    start_q.put(n)

while end_q.qsize() < 10:
    time.sleep(0.0001)

for queue, num in [(start_q, 4), (mid_q, 2), (end_q, 1)]:
    for _ in range(num):
        queue.close()

for better_thread in better_threads:
    better_thread.join()

print(f"Items in end_q: {list(end_q.queue)}")
print(f"Items in mid_q: {list(mid_q.queue)}")
print(f"Items in start_q: {list(start_q.queue)}")

for _ in end_q:
    pass

for queue in [start_q, mid_q, end_q]:
    queue.join()
