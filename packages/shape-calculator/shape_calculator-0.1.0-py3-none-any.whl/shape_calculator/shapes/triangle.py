# Global import
from typing import Union

from src.shape_calculator.arithops_extended import ArithOpsExtended

# Local import
from src.shape_calculator.shapes.shape import Shape


class Triangle(Shape):
    """Represents a triangle, calculating area and perimeter from the abstract class Shape."""

    def __init__(
        self,
        base: Union[float, int],
        height: Union[float, int],
        side1: Union[float, int],
        side2: Union[float, int],
        side3: Union[float, int],
    ):
        """Initializes a Triangle object.

        Args:
        - base (float|int): the length of the base of the triangle
        - height (float|int): the height of the triangle
        - side1 (float|int): the length of the first side of the triangle
        - side2 (float|int): the length of the second side of the triangle
        - side3 (float|int): the length of the third side of the triangle
        """
        self.base = base
        self.height = height
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        self.__check()
        self.arithops = ArithOpsExtended()

    def __check(self):
        """Checks if the input values are valid for a triangle.

        Raises:
            ValueError: If the input values are not positive.
            ValueError: If the input values are invalid for a triangle.
        """
        if (
            self.base <= 0
            or self.height <= 0
            or self.side1 <= 0
            or self.side2 <= 0
            or self.side3 <= 0
        ):
            raise ValueError("Input values should be positive.")
        if (
            self.side1 + self.side2 <= self.base
            or self.side1 + self.side3 <= self.base
            or self.side2 + self.side3 <= self.base
        ):
            raise ValueError("Invalid input values for triangle.")

    def get_area(self) -> Union[float, int]:
        """Calculates the area of the triangle.

        Returns:
            Union[float, int]: The area of the triangle.
        """
        self.arithops.value = self.base
        self.arithops.mul(self.height)
        self.arithops.div(2)
        return self.arithops.value

    def get_perimeter(self) -> Union[float, int]:
        """Calculates the perimeter of the triangle.

        Returns:
            Union[float, int]: The perimeter of the triangle.
        """
        self.arithops.value = 0
        self.arithops.add(self.side1, self.side2, self.side3)
        return self.arithops.value
