import os

import matplotlib.pyplot as plt
import math

def draw_triangle(triangle):
    """Draw and display triangle using matplotlib."""
    a = triangle.base
    h = triangle.height
    angle = triangle.angle_deg

    angle_rad = math.radians(angle)

    # Координаты A и B
    A = (0, 0)
    B = (a, 0)

    # tan(angle) = h / x
    x = h / math.tan(angle_rad)

    C = (x, h)

    x_coords = [A[0], B[0], C[0], A[0]]
    y_coords = [A[1], B[1], C[1], A[1]]

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, color=triangle.color, linewidth=2)
    plt.fill(x_coords, y_coords, triangle.color, alpha=0.4)
    plt.scatter(*zip(A, B, C), color='red')
    plt.axis('equal')
    plt.grid(True)
    plt.title(triangle.label)
    plt.savefig(get_path_to_file("triangle_plot.png"))
    plt.show()

def get_path_to_file(file: str):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', file)



