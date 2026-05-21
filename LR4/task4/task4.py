from task4.shapes import Triangle
from task4.plot import draw_triangle
from utils.inputValidate import input_data


def task4():
    """Main function to run triangle constructor program."""
    while True:
        base = input_data("Input base triangle: ", float, min_value=0)
        height = input_data("Input height: ", float, min_value=0)
        angle = input_data("Input angle (in degrees): ", data_type=float, min_value=0, max_value=180)
        color = input_data("Input color triangle (for example, 'blue', 'green', 'red'...): ", str)
        label = input_data("Input label for triangle: ", str)

        triangle = Triangle(base, height, angle, color, label)
        print(triangle.describe())
        draw_triangle(triangle)

        again = input("\nPrint '1' to repeat or other symbol to exit: ")
        if again != '1':
            break
