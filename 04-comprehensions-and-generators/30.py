from typing import Generator


def iterate_over_scenes(scenes: str) -> Generator[int, None, None]:
    if scenes:
        yield 0
    for i, scene in enumerate(scenes):
        if scene == " ":
            yield i + 1


scenes = "What are you up to today?"

for i in iterate_over_scenes(scenes):
    print(i)
