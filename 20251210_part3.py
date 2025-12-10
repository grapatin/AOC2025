from fetch_advent_input import fetch_advent_input
import re
import time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
example1_result = 33

max_depth = 100
min_depth = max_depth


def solve(input_string: str) -> int:
    lines = input_string.strip().splitlines()
    total = 0
    for line in lines:
        parts = line.split(" ")
        goal_state = parts[-1][1:-1]  # Extract the goal state which is the last part
        parts = parts[1:-1]  # The rest of the parts except last part
        debug_print("Goal:", goal_state)
        button_list = []
        for part in parts:
            button_list.append(part[1:-1].split(","))  # Remove parentheses

        debug_print("Button List:", button_list)

        # remove , from goal_state
        goal_state = tuple(int(x) for x in goal_state.split(","))

        length = len(goal_state)
        equations = []
        results = list(goal_state)
        for button in button_list:
            equation = [0] * length
            for index in map(int, button):
                equation[index] += 1
            equations.append(equation)
        print("Equations:", equations)
        print("Results:", results)

        # Use scipy's integer linear programming
        # Minimize sum of button presses: min c^T x where c = [1, 1, ..., 1]
        c = np.ones(len(equations))

        # Constraint: A^T x = b (where A is equations transposed)
        A = np.array(equations).T
        b = np.array(results)

        constraints = LinearConstraint(A, b, b)  # Equality constraint

        # All variables must be non-negative integers
        bounds = Bounds(0, np.inf)

        # Specify that all variables are integers
        integrality = np.ones(len(equations))

        result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

        if result.success:
            presses = int(np.sum(result.x))
            print("Solution:", result.x, "Total presses:", presses)
            total += presses
        else:
            print("No solution found for line:", line)

    return total


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
problem_input = fetch_advent_input(10)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was:", end_time - start_time, "seconds.")
    print()
