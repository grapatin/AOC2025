from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
example1_result = 4277556


def solve(input_string: str) -> int:
    result = 0
    # Parse input into a 2D list of integers and operators in the last row
    lines = input_string.strip().splitlines()
    grid = []
    operators = []
    for line in lines:
        row = []
        for item in line.split():
            if item in {"*", "+"}:
                operators.append(item)
            else:
                row.append(int(item))
        grid.append(row)

    number_of_tasks = len(operators)
    number_numbers_per_task = len(grid) - 1  # Operators are in operators row
    for task_index in range(number_of_tasks):
        op = operators[task_index]
        numbers_to_calculate = []
        for number_index in range(number_numbers_per_task):
            numbers_to_calculate.append(grid[number_index][task_index])

        if op == "*":
            task_result = 1
            for num in numbers_to_calculate:
                task_result *= num
        elif op == "+":
            task_result = sum(numbers_to_calculate)
        else:
            raise ValueError(f"Unknown operator: {op}")
        print(f"Task {task_index + 1}: Operator {op}, Numbers {numbers_to_calculate} => Result {task_result}")
        result += task_result
    return result


# Test the example
result = solve(example_input)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input, make sure to pass the correct DAY number
problem_input = fetch_advent_input(6)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()
