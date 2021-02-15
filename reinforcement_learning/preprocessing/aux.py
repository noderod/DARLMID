"""
SUMMARY

Auxiliary functions for preprocessor.py, added here to avoid clutter.
"""

import json
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
