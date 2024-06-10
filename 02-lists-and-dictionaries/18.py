class CustomDict(dict[str, str]):

    def __missing__(self, key: str) -> str:
        value = self._create_default(key)
        self[key] = value
        return value

    def _create_default(self, key: str) -> str:
        return f"default_value_for_{key}"


cd = CustomDict()

print(cd["hello"])
