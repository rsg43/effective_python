def transform(a: float, b: float, inverse: bool = False) -> float:
    if inverse:
        return b / a
    return a / b


print(transform(1.0, 2.0))
print(transform(1.0, 2.0, inverse=True))
