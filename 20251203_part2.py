from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = True


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""
example1_result = 3121910778619


def solve(input_string: str) -> int:
    battery_banks = input_string.split("\n")
    # find higest value in first-second to last digit
    sum = 0
    number_of_battery_to_use = 12
    for bank in battery_banks:
        length = len(bank)
        start_pos = 0
        best_pos = start_pos
        current_number = 0
        for number_of_battery in range(number_of_battery_to_use):
            max = -1
            for i in range(start_pos, length - 11 + number_of_battery):
                current_digit = int(bank[i])
                if current_digit > max:
                    max = current_digit
                    best_pos = i

            current_number += max * (10 ** (number_of_battery_to_use - number_of_battery - 1))
            start_pos = best_pos + 1
        debug_print(f"Best number for bank {bank} is {current_number}")
        sum += current_number
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
problem_input = fetch_advent_input(3)

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
