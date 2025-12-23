import pytest

from src.models.chip import Chip


def test_chip_addition_and_errors() -> None:
    chip = Chip(5)
    other = Chip(3)

    assert (chip + other).value == 8
    assert (chip + 5).value == 10
    assert repr(chip) == 'Chip(value=5)'

    with pytest.raises(ValueError):
        Chip(-1)

    with pytest.raises(TypeError):
        _ = chip + 'bad'
