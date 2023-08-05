from typing import Union


class ArithOps:
    """A class that provides four arithmetic operations: addition, subtraction, multiplication, and division."""

    def __init__(self, value: Union[float, int] = 0):
        """Initialize the instance value called `value` for calculating the arithmetic operations.

        Args:
            value (Union[float, int]): Initial value. Defaults to 0.
        """
        self.value = value

    def add(self, value: Union[float, int]):
        """Add the value to instance value called `value`.

        Args:
            value (Union[float, int]): Value to add
        """
        self.value = self.value + value

    def sub(self, value: Union[float, int]):
        """Subtract the value to the instance value called `value`.

        Args:
            value (Union[float, int]): Value to subtract
        """
        self.value = self.value - value

    def mul(self, value: Union[float, int]):
        """Multiply the value to instance value called `value`.

        Args:
            value (Union[float, int]): Value to multiply
        """
        self.value = self.value * value

    def div(self, value: Union[float, int]):
        """Divide the value to the instance value called `value`.

        Args:
            value (Union[float, int]): Value to divide

        Raises:
            ZeroDivisionError: If the value to divide is zero, the calculation is invalid.
        """
        if value == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.value = self.value / value
