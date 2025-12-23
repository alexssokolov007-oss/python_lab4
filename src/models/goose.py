from src.constants import MERGE_HYPE_BONUS
from src.models.player import Player


class Goose:
    """Base goose with a name and honk volume."""

    def __init__(self, name: str, honk_volume: int) -> None:
        self.name = name
        self.honk_volume = honk_volume

    def __add__(self, other: "Goose") -> "Goose":
        """Merge two geese into a flock with boosted volume."""
        if not isinstance(other, Goose):
            raise TypeError("Can only add another Goose.")
        combined_volume = max(self.honk_volume, other.honk_volume) + MERGE_HYPE_BONUS
        return Goose(name=f"{self.name}-{other.name} Flock", honk_volume=combined_volume)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, honk_volume={self.honk_volume})"


class WarGoose(Goose):
    """Goose that attacks players."""

    def attack(self, player: Player, damage: int) -> int:
        """Attack a player and return the actual damage dealt."""
        return player.withdraw(damage)


class HonkGoose(Goose):
    """Goose that can honk to scare players."""

    def __call__(self, player: Player, impact: int) -> int:
        """Honk at a player and return the amount lost."""
        return player.withdraw(impact)
