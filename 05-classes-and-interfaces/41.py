import abc
from typing import Any, Self, Optional

import json


class ToDictMixIn(object):
    def to_dict(self) -> dict[Any, Any]:
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict: dict[Any, Any]) -> dict[Any, Any]:
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key: Any, value: Any) -> Any:
        if isinstance(value, ToDictMixIn):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, val) for val in value]
        elif isinstance(value, tuple):
            return tuple(self._traverse(key, val) for val in value)
        elif isinstance(value, set):
            return {self._traverse(key, val) for val in value}
        elif hasattr(value, "__dict__"):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixIn):
    def __init__(
        self,
        value: int,
        left: Optional[Self] = None,
        right: Optional[Self] = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right


tree = BinaryTree(
    10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)),
)

print(tree.to_dict())
print(tree.__dict__)


class BinaryTreeWithParent(BinaryTree):
    def __init__(
        self,
        value: int,
        left: Optional[Self] = None,
        right: Optional[Self] = None,
        parent: Optional[Self] = None,
    ) -> None:
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key: Any, value: Any) -> Any:
        if isinstance(value, BinaryTreeWithParent) and key == "parent":
            return value.value
        else:
            return super()._traverse(key, value)


root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())


class JSONMixIn:

    @abc.abstractmethod
    def to_dict(self) -> dict[Any, Any]:
        pass

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_json(cls, data: str) -> Self:
        kwargs = json.loads(data)
        return cls(**kwargs)


class Switch(ToDictMixIn, JSONMixIn):
    def __init__(
        self, ports: Optional[int] = None, speed: Optional[float] = None
    ) -> None:
        self.ports = ports
        self.speed = speed


class Machine(ToDictMixIn, JSONMixIn):
    def __init__(
        self,
        cores: Optional[int] = None,
        ram: Optional[int] = None,
        disk: Optional[int] = None,
    ) -> None:
        self.cores = cores
        self.ram = ram
        self.disk = disk


class DatacenterRack(ToDictMixIn, JSONMixIn):
    def __init__(
        self,
        switch: dict[Any, Any],
        machines: Optional[list[dict[Any, Any]]] = None,
    ) -> None:
        self.switch = Switch(**switch)
        self.machines = (
            [Machine(**kwargs) for kwargs in machines] if machines else []
        )


rav_comp = Machine(cores=16, ram=128, disk=1000)
flo_comp = Machine(cores=4, ram=32, disk=500)

rack = DatacenterRack(
    switch={"ports": 5, "speed": 1.0},
    machines=[rav_comp.to_dict(), flo_comp.to_dict()],
)

print(rack.to_dict())
print(rack.to_json())
