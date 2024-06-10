import time
from typing import Iterable
from threading import Thread
import subprocess


print("Factorising numbers")


def factorise(number: int) -> Iterable[int]:
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [3478245, 34932, 45495, 235462]

start = time.time()
for number in numbers:
    list(factorise(number))
delta = time.time() - start
print(f"Serial execution took {delta:.3f} seconds")


class FactoriseThread(Thread):
    def __init__(self, number: int) -> None:
        super().__init__()
        self.number = number

    def run(self) -> None:
        self.factors = list(factorise(self.number))


start = time.time()
factor_threads = [FactoriseThread(number) for number in numbers]
for factor_thread in factor_threads:
    factor_thread.start()

for factor_thread in factor_threads:
    factor_thread.join()
delta = time.time() - start
print(f"Threaded execution took {delta:.3f} seconds")


print("Using a slow system call to simulate blocking I/O operation")


def slow() -> None:
    subprocess.run(["sleep", "0.01"])


def extra() -> None:
    time.sleep(0.1)


start = time.time()
for _ in range(100):
    slow()
extra()
delta = time.time() - start
print(f"Serial execution took {delta:.3f} seconds")

start = time.time()
threads: list[Thread] = []
for _ in range(100):
    thread = Thread(target=slow)
    thread.start()
    threads.append(thread)
extra()
for thread in threads:
    thread.join()
delta = time.time() - start
print(f"Threaded execution took {delta:.3f} seconds")
