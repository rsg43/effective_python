def careful_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError as exc:
        raise ValueError("Invalid inputs") from exc


print(careful_divide(1, 2))
print(careful_divide(1, 0))
