from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
example1_result = 21


def solve(input_string: str) -> int:
    # Parse input into a dict, where (x,y) -> char
    grid = {}
    lines = input_string.splitlines()
    y = 0
    for line in lines:
        x = 0
        for char in line:
            grid[(x, y)] = char
            x += 1
        y += 1
    # Find S as start position
    start_pos = None
    for (x, y), char in grid.items():
        if char == "S":
            start_pos = (x, y)
            break
    beam_positions = set()
    beam_positions.add(start_pos)
    y = start_pos[1] + 1
    split_count = 0
    while y < len(lines):
        new_beam_positions = set()
        for beam_pos in beam_positions:
            x = beam_pos[0]
            current_pos = (x, y)
            if grid.get(current_pos, ".") == "^":
                split_count += 1
                left_pos = (x - 1, y)
                right_pos = (x + 1, y)
                new_beam_positions.add(left_pos)
                new_beam_positions.add(right_pos)
            else:
                new_beam_positions.add(current_pos)
        beam_positions = new_beam_positions
        y += 1
    return split_count


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
problem_input = fetch_advent_input(7)

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
