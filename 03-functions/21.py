def top_scope() -> bool:
    flag = False

    def inner_scope() -> None:
        flag = True  # noqa: F841
        return

    inner_scope()
    return flag


print(top_scope())
