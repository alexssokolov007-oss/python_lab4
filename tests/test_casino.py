import random

from src.casino import Casino
from src.models.goose import Goose, HonkGoose, WarGoose
from src.models.player import Player


def test_casino_events_and_run_step(capsys) -> None:
    rng = random.Random(3)
    casino = Casino(rng)

    alice = Player("Alice", 100)
    boris = Player("Boris", 80)
    casino.register_player(alice)
    casino.register_player(boris)

    war_goose = WarGoose("Warrior", 5)
    honk_goose = HonkGoose("Honker", 4)
    plain_goose = Goose("Plain", 2)
    casino.register_goose(war_goose)
    casino.register_goose(honk_goose)
    casino.register_goose(plain_goose)

    casino._event_place_bet()
    casino._event_bonus()
    casino._event_war_attack()
    casino._event_honk()
    casino._event_steal()
    casino._event_merge_geese()
    casino._event_panic()

    events = casino.available_events()
    assert any(callable(ev) for ev in events)

    casino.run_step(1)
    output = capsys.readouterr().out
    assert "-- Step 1 --" in output


def test_merge_geese_with_insufficient_count(capsys) -> None:
    casino = Casino(random.Random(1))
    casino.register_player(Player("Solo", 10))
    casino.register_goose(Goose("Only", 1))

    casino._event_merge_geese()

    output = capsys.readouterr().out
    assert "Not enough geese to merge." in output


def test_place_bet_without_balance(capsys) -> None:
    casino = Casino(random.Random(2))
    poor_player = Player("Poor", 0)
    casino.register_player(poor_player)
    casino.register_goose(Goose("G", 1))

    casino._event_place_bet()

    output = capsys.readouterr().out
    assert "cannot place a bet" in output
    assert poor_player.balance == 0


def test_available_events_without_special_geese() -> None:
    casino = Casino(random.Random(3))
    casino.register_player(Player("P1", 10))
    casino.register_player(Player("P2", 20))
    casino.register_goose(Goose("Common", 1))

    events = casino.available_events()
    names = {event.__name__ for event in events}

    assert "_event_war_attack" not in names
    assert "_event_honk" not in names
    assert "_event_place_bet" in names


def test_place_bet_loss_branch(capsys) -> None:
    rng = random.Random(2)
    casino = Casino(rng)
    casino.register_player(Player("A", 50))
    casino.register_goose(Goose("G", 1))
    casino.rng.random = lambda: 0.9  # force loss

    casino._event_place_bet()
    out = capsys.readouterr().out
    assert "lost the bet" in out


def test_merge_geese_while_loop(monkeypatch) -> None:
    rng = random.Random(4)
    casino = Casino(rng)
    first = Goose("First", 1)
    second = Goose("Second", 2)
    casino.register_player(Player("P", 10))
    casino.register_goose(first)
    casino.register_goose(second)

    call_log: list[str] = []

    def fake_get_random(*_):
        choice = [first, first, second][len(call_log)]
        call_log.append(choice.name)
        return choice

    monkeypatch.setattr(casino.geese, "get_random", fake_get_random)

    casino._event_merge_geese()
    assert call_log[:2] == ["First", "First"]
    assert len(casino.geese) == 1


def test_bonus_event_increases_balance(capsys) -> None:
    casino = Casino(random.Random(5))
    player = Player("Lucky", 10)
    casino.register_player(player)

    casino.rng.randint = lambda *_: 7
    casino._event_bonus()

    output = capsys.readouterr().out
    assert "Bonus for Lucky: +7" in output
    assert player.balance == 17


def test_war_attack_updates_income() -> None:
    casino = Casino(random.Random(6))
    player = Player("Target", 30)
    goose = WarGoose("Blaster", 3)
    casino.register_player(player)
    casino.register_goose(goose)

    casino.rng.randint = lambda *_: 12
    casino._event_war_attack()

    assert player.balance == 18
    assert casino.goose_income[goose.name] == 12


def test_honk_event_updates_income() -> None:
    casino = Casino(random.Random(7))
    player = Player("Target", 20)
    goose = HonkGoose("Screamer", 4)
    casino.register_player(player)
    casino.register_goose(goose)

    casino.rng.randint = lambda *_: 2
    casino._event_honk()

    assert player.balance == 15
    assert casino.goose_income[goose.name] == 5


def test_steal_event_caps_at_balance() -> None:
    casino = Casino(random.Random(8))
    player = Player("Target", 3)
    goose = Goose("Thief", 1)
    casino.register_player(player)
    casino.register_goose(goose)

    casino.rng.randint = lambda *_: 10
    casino._event_steal()

    assert player.balance == 0
    assert casino.goose_income[goose.name] == 3


def test_panic_event_zeroes_balance(capsys) -> None:
    casino = Casino(random.Random(9))
    player = Player("Panic", 45)
    casino.register_player(player)

    casino._event_panic()
    output = capsys.readouterr().out
    assert "panicked and lost 45" in output
    assert player.balance == 0
