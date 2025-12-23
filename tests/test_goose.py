import random
import pytest

from src.collections_ext.goose_collection import GooseCollection
from src.constants import MERGE_HYPE_BONUS
from src.models.goose import Goose, HonkGoose, WarGoose
from src.models.player import Player


def test_goose_behaviors() -> None:
    goose_a = Goose('Alpha', 2)
    goose_b = Goose('Bravo', 4)

    merged = goose_a + goose_b
    assert merged.name == 'Alpha-Bravo Flock'
    assert merged.honk_volume == 4 + MERGE_HYPE_BONUS

    player = Player('Bob', 20)
    war_goose = WarGoose('Warrior', 3)
    honk_goose = HonkGoose('Honker', 3)

    assert war_goose.attack(player, 7) == 7
    assert honk_goose(player, 5) == 5
    assert player.balance == 8
    assert 'Goose' in repr(merged)


def test_goose_collection_operations_and_filter() -> None:
    g1 = Goose('G1', 1)
    g2 = Goose('G2', 2)
    honk = HonkGoose('Honk', 3)
    collection = GooseCollection([g1, g2, honk])
    collection.add(Goose('G3', 3))

    assert len(collection) == 4
    assert 'G1' in collection and g2 in collection

    sliced = collection[1:]
    assert len(sliced) == 3

    rng = random.Random(0)
    picked = collection.get_random(rng)
    assert picked in collection

    picked_honk = collection.get_random(rng, HonkGoose)
    assert isinstance(picked_honk, HonkGoose)

    collection[0] = honk
    assert collection[0] is honk
    del collection[0]
    assert len(collection) == 3

    collection.add(g1)
    collection.remove(g1)
    assert len(collection) == 3
    assert collection.find_by_name('G2') is g2
    assert collection.find_by_name('Missing') is None
    assert 'goose collection size=' in repr(collection)
    assert 'Z' not in collection
    assert object() not in collection


def test_goose_add_type_error() -> None:
    goose = Goose('Solo', 1)
    with pytest.raises(TypeError):
        _ = goose + 5
