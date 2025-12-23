class Chip:
    """Casino chip with arithmetic support."""

    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError("Chip value must be non-negative.")
        self.value = value

    def __add__(self, other: "Chip | int") -> "Chip":
        """Add chip values with another chip or integer."""
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        if isinstance(other, int):
            return Chip(self.value + other)
        raise TypeError("Chip can only be added to Chip or int.")

    def __repr__(self) -> str:
        return f"Chip(value={self.value})"
