import numpy
from abc import ABC, abstractmethod

class MatrixBase(ABC):
    """Abstract base class for matrix operations."""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.matrix = None

    @abstractmethod
    def generate_matrix(self):
        """Generate a matrix."""
        pass

    def get_matrix(self):
        """Return the matrix."""
        return self.matrix


class MatrixCreator(MatrixBase):
    """Creates integer matrix using random values."""
    def generate_matrix(self):
        """Generate a random integer matrix."""
        self.matrix = numpy.random.randint(-100, 100, (self.rows, self.cols))

    def find_min_elements(self):
        """Return min value and its indices in matrix."""
        min_val = self.matrix.min()
        indices = numpy.argwhere(self.matrix == min_val)
        return min_val, indices


class MatrixAnalyzer:
    """Performs statistical operations on a matrix."""
    def __init__(self, matrix):
        self.matrix = matrix

    def mean(self):
        """Calculate mean of matrix."""
        return numpy.mean(self.matrix)

    def median(self):
        """Calculate median of matrix."""
        return numpy.median(self.matrix)

    def correlation(self):
        """Calculate correlation coefficient matrix."""
        return numpy.corrcoef(self.matrix)

    def variance(self):
        """Calculate variance of matrix."""
        return numpy.var(self.matrix)

    def std_builtin(self):
        """Standard deviation using NumPy."""
        return round(numpy.std(self.matrix), 2)

    def std_manual(self):
        """Standard deviation using manual formula."""
        mean_val = numpy.mean(self.matrix)
        variance = numpy.mean((self.matrix - mean_val) ** 2)
        return round(numpy.sqrt(variance), 2)