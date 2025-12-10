from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
example1_result = 50


def solve(input_string: str) -> int:
    points = []
    lines = input_string.splitlines()
    for line in lines:
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))

    max_rectangle_area = 0
    for point1 in points:
        for point2 in points:
            if point1 == point2:
                continue
            x1, y1 = point1
            x2, y2 = point2
            rectangle_area = abs(x2 - x1 + 1) * abs(y2 - y1 + 1)
            if rectangle_area > max_rectangle_area:
                max_rectangle_area = rectangle_area
    return max_rectangle_area


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
problem_input = fetch_advent_input(9)

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
