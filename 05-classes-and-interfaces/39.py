import os
from typing import Self, Optional, Iterator, Type
from threading import Thread
import random


class BADInputData:
    def read(self) -> str:
        raise NotImplementedError


class BADPathInputData(BADInputData):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def read(self) -> str:
        with open(self.path) as f:
            return f.read()


class BADWorker:
    def __init__(self, input_data: BADInputData) -> None:
        self.input_data = input_data
        self.result: Optional[int] = None

    def map(self) -> None:
        raise NotImplementedError

    def reduce(self, other: Self) -> None:
        raise NotImplementedError


class BADLineCountWorker(BADWorker):
    def map(self) -> None:
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other: BADWorker) -> None:
        if other.result is None or self.result is None:
            raise ValueError("Result is None")
        self.result += other.result


def generate_inputs(data_dir: str) -> Iterator[BADInputData]:
    for name in os.listdir(data_dir):
        yield BADPathInputData(os.path.join(data_dir, name))


def create_workers(
    input_list: Iterator[BADInputData],
) -> list[BADLineCountWorker]:
    workers = []
    for input_data in input_list:
        workers.append(BADLineCountWorker(input_data))
    return workers


def badexecute(workers: list[BADLineCountWorker]) -> int:
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)

    if first.result is None:
        raise ValueError("Result is None")

    return first.result


def badmapreduce(data_dir: str) -> int:
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return badexecute(workers)


def write_test_files(tmpdir: str) -> None:
    os.makedirs(tmpdir, exist_ok=True)
    for i in range(100):
        with open(os.path.join(tmpdir, f"{i}.txt"), "w") as f:
            f.write("\n" * random.randint(0, 100))


tmpdir = "test_inputs"
write_test_files(tmpdir)

result = badmapreduce(tmpdir)
print(f"There are {result} lines")

# ================================


class GenericInputData:
    def read(self) -> str:
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config: dict[str, str]) -> Iterator[Self]:
        raise NotImplementedError


class PathInputData(GenericInputData):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def read(self) -> str:
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config: dict[str, str]) -> Iterator[Self]:
        data_dir = config["data_dir"]
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:

    def __init__(self, input_data: GenericInputData) -> None:
        self.input_data = input_data
        self.result: Optional[int] = None

    def map(self) -> None:
        raise NotImplementedError

    def reduce(self, other: Self) -> None:
        raise NotImplementedError

    @classmethod
    def create_workers(
        cls, input_cls: Type[GenericInputData], config: dict[str, str]
    ) -> list[Self]:
        workers = []
        for input_data in input_cls.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):
    def map(self) -> None:
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other: GenericWorker) -> None:
        if other.result is None or self.result is None:
            raise ValueError("Result is None")
        self.result += other.result


def execute(workers: list[GenericWorker]) -> int:
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)

    if first.result is None:
        raise ValueError("Result is None")

    return first.result


def mapreduce(
    worker_class: Type[GenericWorker],
    input_class: Type[GenericInputData],
    config: dict[str, str],
) -> int:
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


config = {"data_dir": tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f"There are {result} lines")
