class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"{self.name} ({self.age})"


people = [
    Person("Charlie", 35),
    Person("David", 70),
    Person("Alice", 25),
    Person("Bob", 50),
    Person("Eve", 45),
]
print(people)

people.sort(key=lambda x: x.age)
print(people)

people.sort(key=lambda x: x.name)
print(people)
