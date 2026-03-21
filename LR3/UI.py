import Task1
import Task2
import Task3
import Task4
import Task5
import ValidInput
import sys


def repeat_infinity(func):
    """
    Decorator to infinity exec function
    """
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
    return wrapper

@repeat_infinity
def menu():
    """
    Function to display the main menu and execute the selected task.
    """
    
    print("==Menu==")
    print("Choose task:")
    print("1. Task 1")
    print("2. Task 2")
    print("3. Task 3")
    print("4. Task 4")
    print("5. Task 5")
    print("0. Exit")

    n = ValidInput.number(0,5)

    if n==0:
        sys.exit()
        
    if n==4:
        Task4.task()
        return

    print("Choose input method")
    print("1. Manual")
    print("2. Auto (random data)")
    method = ValidInput.number(1,2)


    match n:
        case 1:
            run_task1(method)  
        case 2:
            run_task2(method)  
        case 3:
            run_task3(method)  
        case 5:
            run_task5(method)  

def run_task1(method):  
    """
    Function to get input data to execute Task1.task()
    """
    print("This task find value of ln(1 - x) with eps precise")
    eps = 0
    x = 0
    if method == 2:
        x = next(ValidInput.gen_float(-0.999999999999,0.999999999999))
        eps = next(ValidInput.gen_float(0,1))
        print(f"x: {x}")
        print(f"eps: {eps}") 
    else:
        print("x")
        x = ValidInput.number(-0.999999999999,0.999999999999,float)
        print("eps")
        eps = ValidInput.number(0,1,float)
    try:
        print(Task1.task(x, eps))  
        print("\n")
    except ValueError as e:
        print(f"ERROR: {e}")

def run_task2(method):  
    """
    Function to get input data to execute Task2.task()
    """
    print("Amount of natural even numbers. For exit write 0")
    Task2.task(method)
    return

def run_task3(method):  
    """
    Function to get input data to execute Task3.task()
    """
    s = ""
    print("Find amount of puncto chars in the string")
    if(method == 1):
        s = input("Write string: ")
    if(method == 2):
        s = ValidInput.gen(1,150,str)
        print(s)
    print(Task3.task(s))
    return

def run_task5(method):  
    """
    Function to get input data to execute Task5.task()
    """
    lst = []
    print("Find sum and multiplication of non-negative numbers stayed between absolute min & max elements")
    if(method == 1):
        lst = ValidInput.input_list()
    if(method == 2):
        lst = ValidInput.gen_list()
    print(f"==List==\n{lst}")

    Task5.task(lst)