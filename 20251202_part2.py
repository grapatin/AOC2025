from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = True


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
example1_result = 4174379265


def solve(input_string: str) -> int:
    # check for invalid id but first get a list of id
    ranges = input_string.split(",")

    sum = 0

    for range_ in ranges:
        ids = range_.split("-")

        # check if repeated numbers in id
        start_id = int(ids[0])
        end_id = int(ids[1])
        for id in range(start_id, end_id + 1):
            # check if it consists of repeated sequence
            id_str = str(id)
            length = len(id_str)
            for i in range(1, length // 2 + 1):
                if length % i == 0:
                    segment = id_str[:i]
                    if segment * (length // i) == id_str:
                        sum += id
                        debug_print(f"Found repeated sequence id: {id}")
                        break

    return sum


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
problem_input = fetch_advent_input(2)

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
