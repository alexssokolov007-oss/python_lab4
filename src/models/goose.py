from src.constants import MERGE_HYPE_BONUS
from src.models.player import Player

class Goose:
    """Базовый гусь с именем и громкостью"""
    def __init__(self, name: str, honk_volume: int) -> None:
        self.name = name
        self.honk_volume = honk_volume

    def __add__(self, other: "Goose") -> "Goose":
        """Объединить двух гусей в стаю с усиленной громкостью"""
        if not isinstance(other, Goose):
            raise TypeError("Can only add another Goose.")
        combined_volume = max(self.honk_volume, other.honk_volume) + MERGE_HYPE_BONUS
        return Goose(name=f"{self.name}-{other.name} Flock", honk_volume=combined_volume)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, honk_volume={self.honk_volume})"

class WarGoose(Goose):
    """Гусь, который атакует игроков"""
    def attack(self, player: Player, damage: int) -> int:
        """Атаковать игрока и вернуть фактически нанесенный урон"""
        return player.withdraw(damage)

class HonkGoose(Goose):
    """Гусь, который может кричать и пугать игроков"""
    def __call__(self, player: Player, impact: int) -> int:
        """Крикнуть на игрока и вернуть величину потерь"""
        return player.withdraw(impact)
