# avoid double level comprehensions

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [x for row in matrix for x in row]
print(flattened)

filtered = [x for row in matrix if sum(row) > 10 for x in row if x % 3 == 0]
print(filtered)
