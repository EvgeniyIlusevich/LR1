from task5.matrix_creator import MatrixCreator, MatrixAnalyzer
from utils.inputValidate import input_data

def task5():
    while True:
        rows = input_data("Enter number of rows: ", int, min_value=0)
        cols = input_data("Enter number of columns: ", int, min_value=0)

        matrix_obj = MatrixCreator(rows, cols)
        matrix_obj.generate_matrix()
        matrix = matrix_obj.get_matrix()
        print("\nGenerated matrix:\n", matrix)

        min_val, indices = matrix_obj.find_min_elements()
        print(f"\nMinimum value: {min_val}")
        print(f"Indices of minimum value:\n{indices}")

        analyzer = MatrixAnalyzer(matrix)
        print("\nStatistical Calculations:")
        print("Mean:", analyzer.mean())
        print("Median:", analyzer.median())
        print("Variance:", analyzer.variance())
        print("Standard Deviation (built-in):", analyzer.std_builtin())
        print("Standard Deviation (manual):", analyzer.std_manual())

        again = input("\nPrint '1' to repeat or other symbol to exit: ").lower()
        if again != '1':
            break

