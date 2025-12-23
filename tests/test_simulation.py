from src.simulation import run_simulation


def test_run_simulation_deterministic_output(capsys) -> None:
    run_simulation(steps=3, seed=0)
    output = capsys.readouterr().out

    assert "Casino simulation started." in output
    assert "Using seed=0" in output
    assert "-- Step 1 --" in output
    assert "-- Step 3 --" in output
