from collections.abc import Iterator, MutableMapping

class CasinoBalance(MutableMapping[str, int]):
    """Словарная коллекция балансов с логированием"""
    def __init__(self) -> None:
        self._data: dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self._data[key]

    def __setitem__(self, key: str, value: int) -> None:
        previous = self._data.get(key, 0)
        self._data[key] = value
        print(f"[balance] {key}: {previous} -> {value}")

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def adjust(self, key: str, delta: int) -> int:
        """Изменить баланс на delta и вернуть новое значение"""
        new_value = self._data.get(key, 0) + delta
        self[key] = new_value
        return new_value

    def __repr__(self) -> str:
        return f"CasinoBalance({self._data!r})"
