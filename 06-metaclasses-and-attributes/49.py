from typing import Any, Self
from dataclasses import dataclass

import json


class Serializable:

    def __init__(self, *args: Any) -> None:
        self.args = args

    def serialize(self) -> str:
        return json.dumps({"args": self.args})


class Deserializable(Serializable):

    @classmethod
    def deserialize(cls, data: str) -> Self:
        params = json.loads(data)
        return cls(*params["args"])


class Point2D(Serializable):

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


point_2d = Point2D(5, 3)
print("Object:", point_2d)
print("Serialized:", point_2d.serialize())


class BetterPoint2D(Deserializable):

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"BetterPoint2D({self.x}, {self.y})"


better_point_2d = BetterPoint2D(5, 3)
print("Object:", better_point_2d)
serialized_2d = better_point_2d.serialize()
print("Serialized:", serialized_2d)
deserialized_2d = BetterPoint2D.deserialize(serialized_2d)
print("Deserialized:", deserialized_2d)


class BetterSerializable:

    def __init__(self, *args: Any) -> None:
        self.args = args

    def serialize(self) -> str:
        return json.dumps(
            {"class": self.__class__.__name__, "args": self.args}
        )


class RegisteredSerializable(BetterSerializable):

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        register_class(cls)


registry: dict[str, type[RegisteredSerializable]] = {}


def register_class(target_class: type[RegisteredSerializable]) -> None:
    registry[target_class.__name__] = target_class


def deserialize(data: str) -> BetterSerializable:
    params = json.loads(data)
    return registry[params["class"]](*params["args"])


class Point3D(RegisteredSerializable):

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"


class Point1D(RegisteredSerializable):

    def __init__(self, x: float) -> None:
        super().__init__(x)
        self.x = x

    def __repr__(self) -> str:
        return f"Point1D({self.x})"


point_3d = Point3D(5, 3, -2)
print("Object:", point_3d)
serialized_3d = point_3d.serialize()
print("Serialized:", serialized_3d)
deserialized_3d = deserialize(serialized_3d)
print("Deserialized:", deserialized_3d)

point_1d = Point1D(5)
print("Object:", point_1d)
serialized_1d = point_1d.serialize()
print("Serialized:", serialized_1d)
deserialized_1d = deserialize(serialized_1d)
print("Deserialized:", deserialized_1d)


class Message:

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        register_msg_class(cls)

    def serialize(self) -> str:
        return json.dumps(
            {"class": self.__class__.__name__, "kwargs": self.__dict__}
        )


registry_msg: dict[str, type[Message]] = {}


def register_msg_class(target_class: type[Message]) -> None:
    registry_msg[target_class.__name__] = target_class


def deserialize_msg(data: str) -> Message:
    params = json.loads(data)
    return registry_msg[params["class"]](**params["kwargs"])


@dataclass(frozen=True)
class MyRequest(Message):

    name: str
    age: int


req = MyRequest(name="John", age=30)
print(req.age, req.name)
ser = req.serialize()
print(ser)
deser = deserialize_msg(ser)
print(deser)
