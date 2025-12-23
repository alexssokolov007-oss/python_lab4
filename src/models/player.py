class Player:
    """Игрок казино с балансом"""
    def __init__(self, name: str, balance: int) -> None:
        self.name = name
        self.balance = balance

    def deposit(self, amount: int) -> None:
        """Пополнить баланс на неотрицательную сумму"""
        self.balance += max(0, amount)

    def withdraw(self, amount: int) -> int:
        """Списать до доступного баланса и вернуть фактическую сумму"""
        safe_amount = min(self.balance, max(0, amount))
        self.balance -= safe_amount
        return safe_amount

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, balance={self.balance})"
