from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
example1_result = 3


def solve(input_string: str) -> int:
    current_value = 50
    result = 0
    lines = input_string.splitlines()
    list_of_100_values = []
    for i in range(100):
        list_of_100_values.append(i)
    for line in lines:
        first_char = line[0]
        if first_char == "L":
            current_value -= int(line[1:])
        elif first_char == "R":
            current_value += int(line[1:])
        if list_of_100_values[current_value % 100] == 0:
            result += 1

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

# Call the function and get the problem input
problem_input = fetch_advent_input(1)

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
