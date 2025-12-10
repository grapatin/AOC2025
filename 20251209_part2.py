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
example1_result = 24


class check_if_point_in_polygon:
    def __init__(self, poly_points):
        self.poly_points = poly_points
        self.Xmax = max([p[0] for p in poly_points])
        self.Xmin = min([p[0] for p in poly_points])
        self.Ymax = max([p[1] for p in poly_points])
        self.Ymin = min([p[1] for p in poly_points])

    def first_check(self, x, y):
        if x < self.Xmin or x > self.Xmax or y < self.Ymin or y > self.Ymax:
            return False
        return True

    def on_segment(self, p, q, r) -> bool:
        # Given three collinear points p, q, r, check if point q lies on line segment 'pr'
        if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
            return True
        return False

    def orientation(self, p, q, r) -> int:
        # Calculate the orientation of the triplet (p, q, r)
        # 0 -> p, q and r are collinear
        # 1 -> Clockwise
        # 2 -> Counterclockwise
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def do_intersect(self, p1, p2, r1, r2) -> bool:
        # Check if line segments between p1, p2 and r1, r2 intersect
        o1 = self.orientation(p1, p2, r1)
        o2 = self.orientation(p1, p2, r2)
        o3 = self.orientation(r1, r2, p1)
        o4 = self.orientation(r1, r2, p2)

        # General case - segments properly intersect (cross each other)
        if o1 != o2 and o3 != o4:
            return True

        # For collinear cases, we want to be more careful
        # Only count as intersection if segments actually overlap in their interior
        # Not just touching at endpoints

        # Check if segments are collinear
        if o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0:
            # Both segments are collinear - check if they overlap
            # Get the x and y ranges for both segments
            x1_min, x1_max = min(p1[0], p2[0]), max(p1[0], p2[0])
            y1_min, y1_max = min(p1[1], p2[1]), max(p1[1], p2[1])
            x2_min, x2_max = min(r1[0], r2[0]), max(r1[0], r2[0])
            y2_min, y2_max = min(r1[1], r2[1]), max(r1[1], r2[1])

            # Check if they overlap (not just touch at endpoints)
            x_overlap = max(x1_min, x2_min) < min(x1_max, x2_max)
            y_overlap = max(y1_min, y2_min) < min(y1_max, y2_max)

            # For collinear segments, they overlap if ranges overlap in both dimensions
            # (one dimension will have point overlap, the other needs segment overlap)
            if x1_min == x1_max:  # First segment is vertical
                return x2_min == x1_min and y_overlap
            elif y1_min == y1_max:  # First segment is horizontal
                return y2_min == y1_min and x_overlap
            else:
                # Diagonal segments
                return x_overlap or y_overlap

        return False

    def point_in_polygon(self, x, y) -> bool:
        # Check if the point (x, y) is inside the polygon defined by self.poly_points

        # First check bounding box and skip if outside due to speed reasons
        if not self.first_check(x, y):
            return False

        count = 0
        n = len(self.poly_points)
        for i in range(n):
            next_i = (i + 1) % n
            p1 = self.poly_points[i]
            p2 = self.poly_points[next_i]

            # If the point lies on the polygon edge, consider it inside
            if self.orientation(p1, (x, y), p2) == 0 and self.on_segment(p1, (x, y), p2):
                return True

            # Only consider edges that span the y-coordinate of the test point
            y1, y2 = p1[1], p2[1]

            # Skip edges that don't span y - this prevents double-counting at vertices
            if (y1 <= y and y2 <= y) or (y1 > y and y2 > y):
                continue

            # Calculate x-coordinate of intersection
            x_intersect = p1[0] + (y - y1) * (p2[0] - p1[0]) / (y2 - y1)

            # Only count intersections to the right of the point
            if x_intersect > x:
                count += 1

        # Point is inside if count of intersections is odd
        return count % 2 == 1


def solve(input_string: str) -> int:
    points = []
    lines = input_string.splitlines()
    for line in lines:
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))

    cip = check_if_point_in_polygon(points)
    max_rectangle_area = 0
    for point1 in points:
        for point2 in points:
            if point1 == point2:
                continue
            x1, y1 = point1
            x2, y2 = point2

            xMin = min(x1, x2)
            xMax = max(x1, x2)
            yMin = min(y1, y2)
            yMax = max(y1, y2)

            rectangle_area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if rectangle_area <= max_rectangle_area:
                continue

            # Check if any polygon point is strictly inside the rectangle
            has_point_inside = False
            for p in points:
                if xMin < p[0] < xMax and yMin < p[1] < yMax:
                    has_point_inside = True
                    break

            if has_point_inside:
                continue

            # Check all 4 corners are inside or on the polygon
            all_corners = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
            corners_inside = True
            for corner in all_corners:
                if not cip.point_in_polygon(corner[0], corner[1]):
                    corners_inside = False
                    break

            if not corners_inside:
                continue

            edges_valid = True
            # Check if edges of the rectangle are not passing through a side of the polygon
            # given that we know the polygon is based on straight lines between points
            rectangle_edges = [((x1, y1), (x1, y2)), ((x1, y2), (x2, y2)), ((x2, y2), (x2, y1)), ((x2, y1), (x1, y1))]
            n = len(points)
            for i in range(n):
                next_i = (i + 1) % n
                p1 = points[i]
                p2 = points[next_i]
                for rect_edge in rectangle_edges:
                    if cip.do_intersect(p1, p2, rect_edge[0], rect_edge[1]):
                        edges_valid = False
                        break
                if not edges_valid:
                    break

            if edges_valid:
                max_rectangle_area = rectangle_area
                print(f"New max rectangle area: {rectangle_area} with corners {(x1, y1)} and {(x2, y2)}")

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
    print("Not correct answer is 1796515460")
    print("Not correct answer is 4756718172, too high")
    print("Not correct answer is 2992775188, too high")
    print("Not correct answer is 1775945752, not correct")
    print("Not correct answer is 4599754870, not correct")
    print("Not correct answer is 4599890450, not correct")

    print()
