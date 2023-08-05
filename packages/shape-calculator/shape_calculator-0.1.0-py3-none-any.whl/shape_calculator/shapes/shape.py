from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract class that represents a shape."""

    @abstractmethod
    def get_area(self):
        """Abstract method that calculates the area of a shape."""
        pass

    @abstractmethod
    def get_perimeter(self):
        """Abstract method that calculates the perimeter of a shape."""
        pass

    def __str__(self):
        """Returns a string representation of the shape."""
        return f"Area: {self.get_area()}\nPerimeter: {self.get_perimeter()}"

    def __repr__(self):
        """Returns a string representation of the shape."""
        return self.__str__()

    # def helper(self):
    #     """Helper method that prints the area and perimeter of the shape."""
    #     print(self.__str__())
