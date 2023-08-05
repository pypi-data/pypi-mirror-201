# Global import
from typing import Union

# Local import
from src.shape_calculator.arithops import ArithOps


class ArithOpsExtended(ArithOps):
    """Overrides ArithOps and adds three arithmetic operations: exponentiation, modulus, and floor division."""

    def __check(self, *argv: Union[float, int]):
        """Explicitly checking the validity of the Arithmetic Methods.

        Mainly for testing purposes. Is not run upon instantiation.

        Raises an Error if the value of the fields are not valid.

        Args:
            value (float|int): Value to use one of the ArithOps
        Raises:
            ValueError: If the value to divide is zero or the value to use is zero, the calculation is invalid.
        """
        for arg in argv:
            if arg == 0:
                raise ValueError("Cannot use zero.")

    def add(self, *argv: Union[float, int]):
        """Add the value to instance value called `value`.

        Args:
            value (float|int): Value to add
        """
        for arg in argv:
            self.value += arg

    def sub(self, *argv: Union[float, int]):
        """Subtract the value to the instance value called `value`.

        Args:
            value (float|int): Value to subtract
        """
        for arg in argv:
            self.value -= arg

    def mul(self, *argv: Union[float, int]):
        """Multiply the value to instance value called `value`.

        Args:
            value (float|int): Value to multiply
        """
        for arg in argv:
            self.value *= arg

    def div(self, *argv: Union[float, int]):
        """Divide the value to the instance value called `value`.

        Args:
            value (float|int): Value to divide

        Raises:
            ZeroDivisionError: If the value to divide is zero, the calculation is invalid.
        """
        self.__check(argv)
        for arg in argv:
            self.value /= arg

    def exp(self, *argv: Union[float, int]):
        """Exponentiate the value to instance value called `value`.

        Args:
            value (float|int): Value to exponentiate
        """
        self.__check(self.value)
        for arg in argv:
            self.value = self.value**arg

    def mod(self, *argv: Union[float, int]):
        """Get the remainder of dividing the value to instance value called `value`.

        Args:
            value (float|int): Value to modulus
        """
        self.__check(argv)
        for arg in argv:
            self.value = self.value % arg

    def floordiv(self, *argv: Union[float, int]):
        """Get the floor or the lower number for the value to instance value called `value`.

        Args:
            value (float|int): Value to floor division
        """
        self.__check(argv)
        for arg in argv:
            self.value = self.value // arg
