from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False


# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
example1_result = 25272


def solve(input_string: str) -> int:
    # These are 3d cordinates of points
    junction_boxes = set()
    for line in input_string.splitlines():
        x, y, z = map(int, line.split(","))
        junction_boxes.add((x, y, z))
    circuits = []
    directly_connected = dict()

    # measure distance between all junction boxes and sort them by distance
    added_pairs = set()
    distances = []
    for box1 in junction_boxes:
        for box2 in junction_boxes:
            if box1 == box2:
                continue
            if (box2, box1) in added_pairs:
                continue
            added_pairs.add((box1, box2))
            distance = ((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2) ** 0.5
            distances.append((distance, (box1, box2)))
    distances.sort(key=lambda x: x[0])

    # Find the 2 closest junction boxes in Euclidean distance, do it until all are in one circuit
    i = -1
    while True:
        i += 1
        closest_pair = distances[i][1]

        # if if one box is already in closest_pair is already in a circuit, add the other box to that circuit
        # if both are in different circuits, merge the circuits
        # if both are not in any circuit, create a new circuit
        # if both are in the same circuit, do nothing
        box1_in_circuit = None
        box2_in_circuit = None
        for circuit in circuits:
            if closest_pair[0] in circuit:
                box1_in_circuit = circuit
            if closest_pair[1] in circuit:
                box2_in_circuit = circuit
        if box1_in_circuit is None and box2_in_circuit is None:
            # create new circuit
            circuits.append(set(closest_pair))
        elif box1_in_circuit is not None and box2_in_circuit is None:
            box1_in_circuit.add(closest_pair[1])
        elif box1_in_circuit is None and box2_in_circuit is not None:
            box2_in_circuit.add(closest_pair[0])
        elif box1_in_circuit != box2_in_circuit:
            # merge circuits
            box1_in_circuit.update(box2_in_circuit)
            circuits.remove(box2_in_circuit)
        else:
            # both are in the same circuit, do nothing
            pass

        # Check if all junction boxes are in one circuit
        if len(circuits) == 1 and len(circuits[0]) == len(junction_boxes):
            break

    count = 1
    # find 3 longest circuits
    circuits.sort(key=lambda c: len(c), reverse=True)
    for circuit in circuits[:3]:
        count *= len(circuit)

    return distances[i][1][0][0] * distances[i][1][1][0]


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
problem_input = fetch_advent_input(8)

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
