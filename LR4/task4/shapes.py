from abc import ABC, abstractmethod
from matplotlib.colors import is_color_like

class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the geometric figure."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the geometric figure."""
        pass


class FigureColor:
    """Stores the color of a geometric figure."""

    def __init__(self, color: str):
        self._color = self._validate_color(color)

    @property
    def color(self) -> str:
        """Returns the color of the figure."""
        return self._color

    @color.setter
    def color(self, new_color: str):
        self._color = self._validate_color(new_color)

    @staticmethod
    def _validate_color(color: str) -> str:
        """Validate if a color is valid in Matplotlib."""
        if is_color_like(color):
            return color
        else:
            print(f"Warning: '{color}' is not a valid color. Using default color 'black'\n")
            return "black"


class Triangle(GeometricFigure):
    """Represents a triangle with base, height, and top angle."""

    def __init__(self, base: float, height: float, angle_deg: float, color: str, label: str):
        self.base = base
        self.height = height
        self.angle_deg = angle_deg
        self._color = FigureColor(color)
        self.label = label
        self._name = "Triangle"

    def area(self) -> float:
        """Calculates the area of the triangle."""
        return 0.5 * self.base * self.height

    def get_name(self) -> str:
        return self._name

    def describe(self) -> str:
        """Returns description string using format()."""
        return "\nFigure: {0}\nColor: {1}\nBase: {2}\nHeight: {3}\nangle: {4}°\nrea: {5:.2f}".format(
            self.get_name(), self._color.color, self.base, self.height, self.angle_deg, self.area()
        )

    @property
    def color(self):
        return self._color.color