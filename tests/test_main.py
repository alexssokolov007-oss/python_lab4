import runpy
import sys

import pytest


def test_main_calls_simulation(monkeypatch) -> None:
    from src import main as entrypoint

    called = {}

    def fake_run_simulation(*, steps: int, seed: int | None) -> None:
        called["steps"] = steps
        called["seed"] = seed

    monkeypatch.setattr(entrypoint, "run_simulation", fake_run_simulation)

    exit_code = entrypoint.main(["--steps", "5", "--seed", "42"])
    assert exit_code == 0
    assert called == {"steps": 5, "seed": 42}


def test_main_rejects_non_positive_steps(capsys) -> None:
    from src import main as entrypoint

    exit_code = entrypoint.main(["--steps", "0"])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Steps must be a positive integer." in captured.err


def test_main_module_entrypoint(monkeypatch) -> None:
    called = {}

    def fake_run_simulation(*, steps: int, seed: int | None) -> None:
        called["steps"] = steps
        called["seed"] = seed

    sys.modules.pop("src.main", None)
    monkeypatch.setattr("src.simulation.run_simulation", fake_run_simulation)
    monkeypatch.setattr(sys, "argv", ["prog", "--steps", "1", "--seed", "7"])

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("src.main", run_name="__main__")

    assert excinfo.value.code == 0
    assert called == {"steps": 1, "seed": 7}
