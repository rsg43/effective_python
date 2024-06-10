from typing import Optional, Any


def greet(name: Optional[str] = None) -> str:
    return f"Hello, {name or 'stranger'}!"


print(greet())
print(greet("Alice"))


def default(list_to_return: Optional[list[Any]] = None) -> list[Any]:
    if list_to_return is None:
        list_to_return = []
    return list_to_return


temp_list = [1, 2, 3]
first_list = default()
print(first_list)
new_list = default(temp_list)
print(new_list)
first_list.append(4)
print(first_list)
print(new_list)
