from task1.task1 import task1
from task2.task2 import task2
from task3.task3 import task3
from task4.task4 import task4
from task5.task5 import task5
from task6.task6 import task6
from utils.inputValidate import input_data


# ---------------------------------------------------------
# Lab Work №4
# Version: 1.0
# Objective: to master the basic syntax of the Python language,
# acquire skills in working with files, classes, serializers, regular expressions
# and standard libraries and consolidate them based on the development of interactive applications.
# Developer: Ilusevich Evgeniy
# Date of Development: 10.04.2025
# ---------------------------------------------------------


while True:
    print("\n1. Run task1\n2. Run task2\n3. Run task3\n4. Run task4\n5. Run task5\n6. Run task6\n0. Exit\n")

    select = input_data("Input number of task: ", int, -1, 7)
    match select:
        case 1: task1()
        case 2: task2()
        case 3: task3()
        case 4: task4()
        case 5: task5()
        case 6: task6()
        case _: break
