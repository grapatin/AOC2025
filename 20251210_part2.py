from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
example1_result = 7

max_depth = 10

min_depth = max_depth


def rec_solver(goal, current_state, visited_states, buttons, cache_dict, button_pressed=[], depth=0):
    global min_depth
    if depth > min_depth:
        debug_print("  " * depth + "Exceeded maximum depth, backtracking.")
        return 0

    # check if we reach this state with less depth before
    if current_state in cache_dict:
        if cache_dict[current_state] <= depth:
            debug_print("  " * depth + "Reached this state before with less or equal depth, backtracking.")
            return 0

    # Update cache with current depth (better or first time)
    cache_dict[current_state] = depth

    debug_print("  " * depth + f"Recursion depth {depth}, current_state: {current_state}, goal: {goal}")

    if current_state == goal:
        debug_print("  " * depth + "Goal reached!")
        if depth < min_depth:
            min_depth = depth
            debug_print("  " * depth + f"New minimum depth found: {min_depth}, button presses: {button_pressed}")
        return 1

    if current_state in visited_states:
        debug_print("  " * depth + "Already visited this state, skipping.")
        return 0

    visited_states.add(current_state)
    cache_dict[current_state] = depth

    for button in buttons:
        new_state = list(current_state)
        for index in map(int, button):
            new_state[index] = 1 - new_state[index]  # Toggle the light
        new_state_tuple = tuple(new_state)
        debug_print("  " * depth + f"Pressing button {button} leads to new state: {new_state_tuple}")
        _ = rec_solver(goal, new_state_tuple, visited_states, buttons, cache_dict, button_pressed + [button], depth + 1)

    visited_states.remove(current_state)

    return 1


def solve(input_string: str) -> int:
    lines = input_string.strip().splitlines()
    total = 0
    i = 0
    for line in lines:
        cache_dict = {}
        parts = line.split(" ")
        goal_lights = parts[0][1:-1]  # Extract the light pattern
        parts = parts[1:-1]  # The rest of the parts except last part
        debug_print("Lights:", goal_lights)
        button_list = []
        for part in parts:
            button_list.append(part[1:-1].split(","))  # Remove parentheses

        debug_print("Button List:", button_list)

        # replace # with 1 and . with 0
        goal_lights = goal_lights.replace("#", "1").replace(".", "0")
        goal_state = tuple(int(c) for c in goal_lights)
        start_state = tuple(0 for _ in goal_state)
        visited_states = set()
        _ = rec_solver(goal_state, start_state, visited_states, button_list, cache_dict)
        global min_depth
        print("Result for line:", line, "is", min_depth)
        total += min_depth
        min_depth = max_depth  # Reset for next line
        print("Processing line: ", i)
        i += 1

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
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()
