from typing import Any


scenes: dict[str, list[Any]] = {
    "1": [],
    "2": [],
    "3": [],
    "5": [],
}

if (list_4 := scenes.get("4")) is None:
    scenes["4"] = list_4 = []

list_4.append("In the fourth scene")
scenes = {key: scenes[key] for key in sorted(scenes)}

print(scenes)
