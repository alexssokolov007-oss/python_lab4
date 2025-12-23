import random

from src.casino import Casino
from src.constants import DEFAULT_GOOSE, DEFAULT_PLAYERS
from src.models.goose import HonkGoose, WarGoose
from src.models.player import Player


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    """
    Запуск псевдослучайной симуляции казино

    При заданном seed последовательность событий повторяется
    """
    rng = random.Random(seed)
    casino = Casino(rng)

    for name, balance in DEFAULT_PLAYERS:
        casino.register_player(Player(name=name, balance=balance))

    for name, volume, kind in DEFAULT_GOOSE:
        goose = WarGoose(name, volume) if kind == "war" else HonkGoose(name, volume)
        casino.register_goose(goose)

    print("Casino simulation started.")
    if seed is not None:
        print(f"Using seed={seed}")

    for step in range(1, steps + 1):
        casino.run_step(step)
