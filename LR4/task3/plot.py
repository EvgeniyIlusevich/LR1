import os
import matplotlib.pyplot as plt

def plot_series_vs_math(fx_values: list[float], math_fx: float):
    """Plot the function approximation vs the actual math function."""
    n_values = list(range(1, len(fx_values) + 1))
    math_fx_line = [math_fx for _ in n_values]

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, fx_values, label="Series Approximation F(x)", color="blue", marker='o')
    plt.plot(n_values, math_fx_line, label="Math F(x)", color="red", linestyle="--")

    plt.title("Comparison of Series Approximation and Math Function")
    plt.xlabel("Number of Terms (n)")
    plt.ylabel("Function Value")
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plt.annotate(f"True F(x) = {math_fx:.5f}", xy=(n_values[-1], math_fx),
                 xytext=(n_values[-1], math_fx + 0.5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.tight_layout()
    plt.savefig(get_path_to_file("function_plot.png"))
    plt.show()


def get_path_to_file(file: str):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', file)