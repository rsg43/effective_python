from dataclasses import dataclass


@dataclass(frozen=True)
class Grade:
    score: float
    weight: float


class Subject:
    def __init__(self, name: str) -> None:
        self.name = name
        self._grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        self._grades.append(grade)

    def average_grade(self) -> float:
        total = 0.0
        total_weight = 0.0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self._subjects: dict[str, Subject] = {}

    def add_subject(self, subject: Subject) -> None:
        self._subjects[subject.name] = subject

    def get_subject(self, name: str) -> Subject:
        return self._subjects[name]

    def average_grade(self) -> float:
        total = 0.0
        total_weight = 0.0
        for subject in self._subjects.values():
            total += subject.average_grade()
            total_weight += 1.0
        return total / total_weight


class Gradebook:
    def __init__(self) -> None:
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        self._students[student.name] = student

    def get_student(self, name: str) -> Student:
        return self._students[name]

    def average_grade(self) -> float:
        total = 0.0
        total_weight = 0.0
        for student in self._students.values():
            total += student.average_grade()
            total_weight += 1.0
        return total / total_weight


book = Gradebook()
rav = Student("Rav")
book.add_student(rav)
math = Subject("Math")
math.add_grade(Grade(90, 0.5))
math.add_grade(Grade(80, 0.5))
rav.add_subject(math)
print(book.average_grade())
