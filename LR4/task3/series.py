from statistics import mean, median, mode, variance, stdev

class BaseSeries:
    """Abstract base class for series calculations."""
    def __init__(self, x: float, eps: float):
        self.x = x
        self.eps = eps
        self.n = 0
        self.fx = 0
        self.math_fx = 0
        self.terms = []

    def calculate(self):
        raise NotImplementedError("Must implement calculate method")

    def get_results(self):
        return self.x, self.n, self.fx, self.math_fx, self.eps


class SeriesCalculator(BaseSeries):
    """Calculator for computing power series expansion of 1 / (1 - x)."""
    MAX_ITERATION = 500

    def calculate(self):
        self.math_fx = 1 / (1 - self.x)

        term = 1
        self.fx = term
        self.terms = [term]
        self.n = 1

        while self.n < self.MAX_ITERATION:
            term *= self.x
            if abs(term) < self.eps:
                break
            self.fx += term
            self.terms.append(self.fx)
            self.n += 1

    def get_statistics(self) -> dict:
        """Calculate and return statistical measures of the series terms."""
        if len(self.terms) < 2:
            raise Exception("Not enough data points to calculate statistics")

        return {
            "Mean": mean(self.terms),
            "Median": median(self.terms),
            "Mode": mode(self.terms),
            "Variance": variance(self.terms),
            "Stdev": stdev(self.terms),
        }