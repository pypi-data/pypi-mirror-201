# Global import
from typing import Union

from src.shape_calculator.arithops_extended import ArithOpsExtended

# Local import
from src.shape_calculator.shapes.shape import Shape


class Rectangle(Shape):
    """Represents a rectangle, calculating area and perimeter from the abstract class Shape."""

    def __init__(self, length: Union[float, int], width: Union[float, int]):
        """Initializes a Rectangle object.

        Args:
        - length (float|int): the length of the rectangle
        - width (float|int): the width of the rectangle
        """
        self.length = length
        self.width = width
        self.__check()
        self.arithops = ArithOpsExtended()

    def __check(self):
        """Checks if the input values are valid for a triangle.

        Raises:
            ValueError: If the input values are not positive.
        """
        if self.length <= 0 or self.width <= 0:
            raise ValueError("Input values should be positive.")

    def get_area(self) -> Union[float, int]:
        """Calculates the area of the rectangle.

        Returns:
            Union[float, int]: The area of the rectangle.
        """
        self.arithops.value = self.length
        self.arithops.mul(self.width)
        return self.arithops.value

    def get_perimeter(self) -> Union[float, int]:
        """Calculates the perimeter of the rectangle.

        Returns:
            Union[float, int]: The perimeter of the rectangle.
        """
        self.arithops.value = self.length
        self.arithops.add(self.width)
        self.arithops.mul(2)
        return self.arithops.value
