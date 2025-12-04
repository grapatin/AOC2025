from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = True


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
example1_result = 43


def solve(input_string: str) -> int:
    # Parse the input into a dictionary of coordinates with chars
    grid = {}
    x, y = 0, 0
    for line in input_string.split("\n"):
        x = 0
        for char in line:
            grid[(x, y)] = char
            x += 1
        y += 1

    # check each position with @ and count how many @ are adjacent (including diagonals)
    total_movable_rolls = 0
    while True:
        movable_rolls = 0
        removable_rolls = set()
        for (x, y), char in grid.items():
            count = 0
            if char == "@":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        neighbor = (x + dx, y + dy)
                        if neighbor in grid and grid[neighbor] == "@":
                            count += 1
                debug_print(f"Position ({x},{y}) has {count} adjacent '@'")
                if count < 4:
                    movable_rolls += 1
                    removable_rolls.add((x, y))
                    total_movable_rolls += 1
        if movable_rolls == 0:
            break
        for pos in removable_rolls:
            del grid[pos]

    # print the final grid
    max_x = max(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys())
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in grid:
                line += grid[(x, y)]
            else:
                line += "."
        debug_print(line)

    return total_movable_rolls


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
problem_input = fetch_advent_input(4)

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
