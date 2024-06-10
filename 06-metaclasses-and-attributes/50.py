from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Field(str, Generic[T]):

    def __init__(self, name: str) -> None:
        self.name = name
        self.internal_name = "_" + self.name

    def __get__(self, instance: T, instance_type: type[T]) -> str:
        _ = instance_type
        if instance is None:
            return self
        return getattr(instance, self.internal_name, "")

    def __set__(self, instance: T, value: str) -> None:
        setattr(instance, self.internal_name, value)


class Customer:

    first_name: str = Field("first_name")
    last_name: str = Field("last_name")
    prefix: str = Field("prefix")
    suffix: str = Field("suffix")


customer = Customer()
print(customer.__dict__)
customer.first_name = "John"
print(customer.__dict__)


class BetterField(str, Generic[T]):

    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.internal_name: Optional[str] = None

    def __set_name__(self, owner: type[T], name: str) -> None:
        _ = owner
        self.name = name
        self.internal_name = "_" + self.name

    def __get__(self, instance: T, instance_type: type[T]) -> str:
        _ = instance_type
        if instance is None:
            return self
        if self.internal_name is None:
            raise ValueError("internal_name is not set")

        return getattr(instance, self.internal_name, "")

    def __set__(self, instance: T, value: str) -> None:
        if self.internal_name is None:
            raise ValueError("internal_name is not set")

        setattr(instance, self.internal_name, value)


class BetterCustomer:

    first_name: str = BetterField()
    last_name: str = BetterField()
    prefix: str = BetterField()
    suffix: str = BetterField()


better_customer = BetterCustomer()
print(better_customer.__dict__)
better_customer.first_name = "John"
print(better_customer.__dict__)
