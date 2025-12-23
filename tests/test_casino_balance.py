from src.collections_ext.casino_balance import CasinoBalance


def test_casino_balance_logs_and_adjusts(capsys) -> None:
    balances = CasinoBalance()
    balances['Alice'] = 10
    balances.adjust('Alice', 5)
    balances.adjust('Bob', 7)

    output = capsys.readouterr().out
    assert '[balance] Alice: 0 -> 10' in output
    assert '[balance] Bob: 0 -> 7' in output
    assert balances['Alice'] == 15
    assert 'CasinoBalance' in repr(balances)


def test_casino_balance_iter_and_delete() -> None:
    balances = CasinoBalance()
    balances['A'] = 1
    balances['B'] = 2

    keys = set(iter(balances))
    assert keys == {'A', 'B'}

    del balances['A']
    assert len(balances) == 1
    assert list(balances)[0] == 'B'
