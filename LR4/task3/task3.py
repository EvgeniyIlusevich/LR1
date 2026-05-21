from tabulate import tabulate
from task3.series import SeriesCalculator
from task3.plot import plot_series_vs_math
from utils.inputValidate import input_data

def print_description():
    """Print description of the task."""
    print("""
This program calculates the value of the function 1 / (1 - x)
using power series expansion, compares it with the value from the math function,
and plots both on a single graph.
    """)


def task3():
    """Main loop for user interaction and execution."""
    while True:
        print_description()

        eps = input_data("Enter epsilon (0 < eps < 1): ", float, min_value=0, max_value=1)
        x = input_data("Enter x (-1 < x < 1): ", float, min_value=-1, max_value=1)

        try:
            calc = SeriesCalculator(x, eps)
            calc.calculate()

            x_val, n, fx, math_fx, eps = calc.get_results()
            stats = calc.get_statistics()

            print("\n--- Results ---")
            print(tabulate([[x_val, n, fx, math_fx, eps]],
                           headers=["x", "n", "F(x)", "Math F(x)", "eps"],
                           tablefmt="grid", floatfmt=".10f"))

            print("\n--- Statistics of Series Terms ---")
            for key, val in stats.items():
                print(f"{key}: {val:.10f}")

            plot_series_vs_math(calc.terms, math_fx)
        except Exception as e:
            print(e)

        again = input("\nPrint '1' to repeat or other symbol to exit: ")
        if again != '1':
            break
