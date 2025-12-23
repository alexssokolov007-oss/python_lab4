class Player:
    """Casino player with a balance."""

    def __init__(self, name: str, balance: int) -> None:
        self.name = name
        self.balance = balance

    def deposit(self, amount: int) -> None:
        """Increase balance by a non-negative amount."""
        self.balance += max(0, amount)

    def withdraw(self, amount: int) -> int:
        """Withdraw up to the current balance and return the actual amount."""
        safe_amount = min(self.balance, max(0, amount))
        self.balance -= safe_amount
        return safe_amount

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, balance={self.balance})"
