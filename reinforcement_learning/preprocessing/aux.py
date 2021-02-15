"""
SUMMARY

Auxiliary functions for preprocessor.py, added here to avoid clutter.
"""

from copy import deepcopy
import json
from math import cos, sin
import sys

from shapely.geometry import Point, Polygon


# Exits the program with an error message and an exit code of 1
def exit_program(error_message):
    sys.exit(error_message)



# Reads a JSON file into a dict
# Assumed that the file exists, if not, an error will be thrown
# If not allowed, it raises an error
def JSON_to_dict(filepath):

    with open(filepath, "r") as jf:
        try:
            return json.load(jf)
        except:
            exit_program("Could not open JSON file")



# Generic obstacle
# Not to be used directly
class Obstacle:

    # Checks if a point insects with it or is contained by it
    # p -> [x, y]
    def collides_with(self, p):

        sp = Point(p[0], p[1])
        return self.shapely_object.intersects(sp) or self.shapely_object.contains(sp)





# Circle obstacle
class Circle_obstacle(Obstacle):

    """
    ID: ID associated with the object
    """
    def __init__(self, center, r):
        self.cx = center[0]
        self.cy = center[1]
        self.r = r

        if r <= 0:
            sys.exit("Radius must be positive. Currently, r = " + str(r))

        self.shapely_object = Point(center[0], center[1]).buffer(r)

    """
    Obtains the center
    """
    def get_center(self):
        return [self.cx, self.cy]



# Polygon obstacle
class Polygon_obstacle(Obstacle):

    """
    ID: ID associated with the object
    """
    def __init__(self, points):
        self.points = [(cord[0], cord[1]) for cord in points]
        self.shapely_object = Polygon(self.points)

        if not self.shapely_object.is_valid:
            sys.exit("Invalid polygon, self-intersect found")



# Generates the collision matrix for a certain position
# 0: Collision at this point (either with an obstacle or the wall)
# 1: empty
# checkable_vectors: Matrix containing the points where to be checked at (0, 0) with a rotation of 0
def compute_collision_matrix(checkable_vectors, total_obstacles, xs, ys, θ, divisions_x, divisions_y):

    updatable_matrix = deepcopy(checkable_vectors)

    for row in range(0, divisions_x):
        for col in range(0, divisions_y):

            original_vector = checkable_vectors[row][col]
            x_v0 = original_vector[0]
            y_v0 = original_vector[1]

            x_v1 = x_v0 + cos(θ)*x_v0 - sin(θ)*y_v0
            y_v1 = y_v0 + sin(θ)*x_v0 + cos(θ)*y_v0

            # Checks if this point collides with the wall
            if not is_within_map(x_v1, y_v1):
                updatable_matrix[row][col] = 0
                continue


            pxy = [x_v1, y_v1]

            # Checks if the point collides with any object
            for an_obstacle in total_obstacles:
                if an_obstacle.collides_with(pxy):
                    updatable_matrix[row][col] = 0
                    break
            else:
                # No collisions
                updatable_matrix[row][col] = 1

    return updatable_matrix



# Checks if a point is within the map
def is_within_map(x, y):

    within_x = (0 <= x) and (x <= 100)
    within_y = (0 <= y) and (y <= 100)

    return within_x and within_y
