import argparse
import sys

from src.simulation import run_simulation


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Casino and geese simulation")
    parser.add_argument("--steps", type=int, default=20, help="number of simulation steps")
    parser.add_argument("--seed", type=int, default=None, help="random seed (optional)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.steps <= 0:
        print("Steps must be a positive integer.", file=sys.stderr)
        return 2
    run_simulation(steps=args.steps, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
