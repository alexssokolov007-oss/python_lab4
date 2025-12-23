import random
from collections.abc import Callable

from src.collections_ext.casino_balance import CasinoBalance
from src.collections_ext.goose_collection import GooseCollection
from src.collections_ext.player_collection import PlayerCollection
from src.constants import (
    BONUS_MAX,
    BONUS_MIN,
    CHIP_BASE_VALUE,
    HONK_IMPACT,
    MAX_BET,
    MERGE_HYPE_BONUS,
    MIN_BET,
    STEAL_MAX,
    STEAL_MIN,
    WAR_GOOSE_MAX_DAMAGE,
    WAR_GOOSE_MIN_DAMAGE,
    WIN_MULTIPLIER,
)
from src.models.chip import Chip
from src.models.goose import Goose, HonkGoose, WarGoose
from src.models.player import Player


class Casino:
    """Состояние казино и набор событий"""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = CasinoBalance()
        self.goose_income = CasinoBalance()

    def register_player(self, player: Player) -> None:
        self.players.add(player)
        self.balances[player.name] = player.balance

    def register_goose(self, goose: Goose) -> None:
        self.geese.add(goose)
        self.goose_income[goose.name] = self.goose_income.get(goose.name, 0)

    def _update_balance(self, player: Player) -> None:
        self.balances[player.name] = player.balance

    def _log(self, message: str) -> None:
        print(message)

    def _event_place_bet(self) -> None:
        player = self.players.get_random(self.rng)
        base_chip = Chip(CHIP_BASE_VALUE)
        extra_chip = base_chip + self.rng.randint(0, CHIP_BASE_VALUE)
        bet_amount = min(player.balance, self.rng.randint(MIN_BET, MAX_BET) + extra_chip.value)
        if bet_amount <= 0:
            self._log(f"{player.name} cannot place a bet without chips.")
            return
        player.withdraw(bet_amount)
        if self.rng.random() < 0.5:
            win_amount = int(bet_amount * WIN_MULTIPLIER)
            player.deposit(win_amount)
            outcome = f"won {win_amount}"
        else:
            outcome = "lost the bet"
        self._update_balance(player)
        self._log(f"{player.name} bet {bet_amount} and {outcome}. Balance: {player.balance}")

    def _event_bonus(self) -> None:
        player = self.players.get_random(self.rng)
        bonus = self.rng.randint(BONUS_MIN, BONUS_MAX)
        player.deposit(bonus)
        self._update_balance(player)
        self._log(f"Bonus for {player.name}: +{bonus}. Balance: {player.balance}")

    def _event_war_attack(self) -> None:
        goose = self.geese.get_random(self.rng, WarGoose)
        player = self.players.get_random(self.rng)
        damage = self.rng.randint(WAR_GOOSE_MIN_DAMAGE, WAR_GOOSE_MAX_DAMAGE)
        inflicted = goose.attack(player, damage)
        self._update_balance(player)
        self.goose_income.adjust(goose.name, inflicted)
        self._log(
            f"{goose.name} attacked {player.name} for {inflicted}. Player balance: {player.balance}"
        )

    def _event_honk(self) -> None:
        goose = self.geese.get_random(self.rng, HonkGoose)
        player = self.players.get_random(self.rng)
        lost = goose(player, HONK_IMPACT + self.rng.randint(0, HONK_IMPACT))
        self._update_balance(player)
        self.goose_income.adjust(goose.name, lost)
        self._log(
            f"{goose.name} honked at {player.name}, lost {lost}. Player balance: {player.balance}"
        )

    def _event_steal(self) -> None:
        goose = self.geese.get_random(self.rng)
        player = self.players.get_random(self.rng)
        to_steal = self.rng.randint(STEAL_MIN, STEAL_MAX)
        stolen = player.withdraw(to_steal)
        self._update_balance(player)
        self.goose_income.adjust(goose.name, stolen)
        self._log(
            f"{goose.name} stole {stolen} from {player.name}. Player balance: {player.balance}"
        )

    def _event_merge_geese(self) -> None:
        if len(self.geese) < 2:
            self._log("Not enough geese to merge.")
            return
        first = self.geese.get_random(self.rng)
        second = self.geese.get_random(self.rng)
        while second is first:
            second = self.geese.get_random(self.rng)
        merged = first + second
        self.geese.remove(first)
        self.geese.remove(second)
        self.register_goose(merged)
        self._log(
            f"Merged {first.name} and {second.name} into {merged.name} (+{MERGE_HYPE_BONUS} volume)."
        )

    def _event_panic(self) -> None:
        player = self.players.get_random(self.rng)
        lost = player.withdraw(player.balance)
        self._update_balance(player)
        self._log(f"{player.name} panicked and lost {lost}. Balance: {player.balance}")

    def available_events(self) -> list[Callable[[], None]]:
        events: list[Callable[[], None]] = [
            self._event_place_bet,
            self._event_bonus,
            self._event_steal,
            self._event_merge_geese,
            self._event_panic,
        ]
        if any(isinstance(goose, WarGoose) for goose in self.geese):
            events.append(self._event_war_attack)
        if any(isinstance(goose, HonkGoose) for goose in self.geese):
            events.append(self._event_honk)
        return events

    def run_step(self, step_index: int) -> None:
        """Выбрать и выполнить одно случайное событие"""
        event = self.rng.choice(self.available_events())
        self._log(f"\n-- Step {step_index} --")
        event()
