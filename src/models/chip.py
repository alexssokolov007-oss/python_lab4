class Chip:
    """Фишка казино с поддержкой арифметики"""
    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError("Значение фишки должно быть неотрицательным")
        self.value = value

    def __add__(self, other: "Chip | int") -> "Chip":
        """Сложить фишки с другой фишкой или целым числом"""
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        if isinstance(other, int):
            return Chip(self.value + other)
        raise TypeError("Фишку можно складывать только с Chip или int")

    def __repr__(self) -> str:
        return f"Chip(value={self.value})"
