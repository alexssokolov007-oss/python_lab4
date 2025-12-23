import random
from collections.abc import Iterable, Iterator

from src.models.player import Player


class PlayerCollection:
    """Списковая коллекция игроков"""

    def __init__(self, players: Iterable[Player] | None = None) -> None:
        self._players: list[Player] = list(players) if players is not None else []

    def add(self, player: Player) -> None:
        self._players.append(player)

    def remove_by_name(self, name: str) -> None:
        self._players = [player for player in self._players if player.name != name]

    def __iter__(self) -> Iterator[Player]:
        return iter(self._players)

    def __len__(self) -> int:
        return len(self._players)

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Player):
            return any(p.name == item.name for p in self._players)
        if isinstance(item, str):
            return any(p.name == item for p in self._players)
        return False

    def __getitem__(self, index):
        if isinstance(index, slice):
            return PlayerCollection(self._players[index])
        return self._players[index]

    def __setitem__(self, index: int, player: Player) -> None:
        self._players[index] = player

    def __delitem__(self, index: int) -> None:
        del self._players[index]

    def get_random(self, rng: random.Random) -> Player:
        return rng.choice(self._players)

    def find_by_name(self, name: str) -> Player | None:
        """Найти игрока по имени"""
        for player in self._players:
            if player.name == name:
                return player
        return None

    def __repr__(self) -> str:
        return f"PlayerCollection({self._players!r})"
