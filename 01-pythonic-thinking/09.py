def all_even(numbers: list[int]) -> bool:
    for number in numbers:
        if number % 2 != 0:
            return False
    return True


print(all_even([0, 2, 4, 6, 8]))
print(all_even([0, 2, 4, 6, 7]))
