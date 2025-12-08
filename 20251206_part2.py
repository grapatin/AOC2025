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
example1_result = 3263827


def solve(input_string: str) -> int:
    result = 0
    # parse input into a x, y dictionary
    lines = input_string.splitlines()

    grid = {}
    y = 0
    for line in lines:
        x = 0
        row = []
        for item in line:
            grid[(x, y)] = item
            x += 1
        y += 1
    number_numbers_per_task = y - 1
    operators_row = y - 1

    # Parse grid and a collumn with only ' ' should have have ','
    length_x = len(lines[0])
    for x in range(length_x):
        all_spaces = True
        for y in range(number_numbers_per_task + 1):
            if grid[(x, y)] != " ":
                all_spaces = False
                break
        if all_spaces:
            for y in range(number_numbers_per_task + 1):
                grid[(x, y)] = ","

    # Now replace all ' ' with 0
    for x in range(length_x):
        for y in range(number_numbers_per_task):
            if grid[(x, y)] == " ":
                grid[(x, y)] = "0"

    # Now duplicate operators until a ',' is found
    current_operator = None
    for x in range(len(lines[operators_row])):
        char = grid[(x, operators_row)]
        if current_operator is None:
            if char in {"*", "+"}:
                current_operator = char
        else:
            if char == ",":
                current_operator = None
            else:
                grid[(x, operators_row)] = current_operator

    print("Parsed grid:")
    for y in range(number_numbers_per_task + 1):
        row = []
        for x in range(len(lines[y])):
            row.append(grid[(x, y)])
        print(" ".join(row))
    column_temp = 0
    # create the new numbers from right to left
    for x in range(len(lines[operators_row]) - 1, -1, -1):
        if grid[(x, operators_row)] == ",":
            result += column_temp
            print(f"New column found {column_temp} and result: {result}")
            column_temp = 0
            continue
        new_number_str = ""
        for y in range(number_numbers_per_task):
            if grid[(x, y)] == "0":
                continue
            new_number_str += grid[(x, y)]
        operator = grid[(x, operators_row)]
        if operator == "*":
            print(f"Multiplying by {new_number_str}")
            if column_temp == 0:
                column_temp = int(new_number_str)
            else:
                column_temp *= int(new_number_str)
        else:
            print(f"Adding {new_number_str}")
            column_temp += int(new_number_str)

    result += column_temp
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
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()
