from typing import Any


class LazyRecord:

    def __init__(self) -> None:
        self.exists = 5

    def __getattribute__(self, name: str) -> Any:
        print(f"__getattribute__ called with {name}")
        try:
            value = super().__getattribute__(name)
            print("Exists!")
            return value
        except AttributeError:
            print("Doesn't exist!")
            value = f"Value for {name}"
            setattr(self, name, value)
            return value

    def __setattr__(self, name: str, value: Any) -> None:
        print(f"__setattr__ called with {name} and {value}")
        super().__setattr__(name, value)


record = LazyRecord()
print(record.exists)
print(record.foo)
print(record.foo)
record.bar = 10
print(record.bar)
