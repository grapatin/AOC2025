from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
example1_result = 14


def solve(input_string: str) -> int:
    part1, _ = input_string.strip().split("\n\n")

    ranges = []
    for line in part1.splitlines():
        start, end = map(int, line.split("-"))
        ranges.append((start, end))
    ranges.sort()

    # Merge overlapping ranges
    merged_ranges = []
    for start, end in ranges:
        size_of_merged_ranges = len(merged_ranges)
        if size_of_merged_ranges == 0:
            merged_ranges.append((start, end))
        else:
            last_start, last_end = merged_ranges[-1]
            if start <= last_end + 1:
                # Overlapping or contiguous ranges, merge them
                merged_ranges[-1] = (last_start, max(last_end, end))
            else:
                merged_ranges.append((start, end))

    fresh_count = 0
    for start, end in merged_ranges:
        fresh_count += end - start + 1

    return fresh_count


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
problem_input = fetch_advent_input(5)

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
