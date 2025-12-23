import random
from collections.abc import Iterable, Iterator

from src.models.goose import Goose


class GooseCollection:
    """Списковая коллекция гусей с простым поиском"""

    def __init__(self, geese: Iterable[Goose] | None = None) -> None:
        self._geese: list[Goose] = list(geese) if geese is not None else []

    def add(self, goose: Goose) -> None:
        self._geese.append(goose)

    def remove(self, goose: Goose) -> None:
        self._geese = [item for item in self._geese if item is not goose]

    def __iter__(self) -> Iterator[Goose]:
        return iter(self._geese)

    def __len__(self) -> int:
        return len(self._geese)

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Goose):
            return any(g.name == item.name for g in self._geese)
        if isinstance(item, str):
            return any(g.name == item for g in self._geese)
        return False

    def __getitem__(self, index):
        if isinstance(index, slice):
            return GooseCollection(self._geese[index])
        return self._geese[index]

    def __setitem__(self, index: int, goose: Goose) -> None:
        self._geese[index] = goose

    def __delitem__(self, index: int) -> None:
        del self._geese[index]

    def get_random(self, rng: random.Random, cls=None):
        """Выбрать случайного гуся, при необходимости по типу"""
        candidates = [goose for goose in self._geese if cls is None or isinstance(goose, cls)]
        return rng.choice(candidates)

    def find_by_name(self, name: str) -> Goose | None:
        """Найти гуся по имени"""
        for goose in self._geese:
            if goose.name == name:
                return goose
        return None

    def __repr__(self) -> str:
        return f"goose collection size={len(self)}"
