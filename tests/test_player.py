import random

from src.collections_ext.player_collection import PlayerCollection
from src.models.player import Player


def test_player_deposit_withdraw_and_repr() -> None:
    player = Player('Test', 50)
    player.deposit(25)
    player.deposit(-10)
    withdrawn = player.withdraw(100)

    assert withdrawn == 75
    assert player.balance == 0
    assert 'Test' in repr(player)


def test_player_collection_behaviour() -> None:
    p1 = Player('Alice', 10)
    p2 = Player('Bob', 20)
    collection = PlayerCollection([p1])
    collection.add(p2)
    collection.remove_by_name('Missing')

    assert len(collection) == 2
    assert collection[0] is p1 and collection[1] is p2

    subset = collection[1:]
    assert isinstance(subset, PlayerCollection)

    rng = random.Random(1)
    chosen = collection.get_random(rng)
    assert chosen in collection

    collection[0] = p2
    assert collection[0] is p2
    del collection[0]
    assert len(collection) == 1

    assert 'Alice' not in collection
    collection.remove_by_name('Alice')
    assert 'Random' not in collection
    assert object() not in collection
    assert 'PlayerCollection' in repr(collection)


def test_player_collection_iter_and_find() -> None:
    p1 = Player('Alice', 10)
    p2 = Player('Bob', 20)
    collection = PlayerCollection([p1, p2])

    names = [player.name for player in collection]
    assert names == ['Alice', 'Bob']

    assert collection.find_by_name('Bob') is p2
    assert collection.find_by_name('Missing') is None
