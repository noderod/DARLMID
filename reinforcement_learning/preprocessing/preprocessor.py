"""
SUMMARY

Pre-processes a JSON file obtained from the server, verifying that all the information is there.
Then, it creates a map and tracks the movements and actions there.
It produces another JSON file with a series of matrices composed of 0 and 1, representing whether or not a certain location is occupied
by an object or outside the map
"""

import argparse
import datetime
import json
import math

import matplotlib.pyplot as plt
import numpy as np

import aux



# Processes arguments
parser = argparse.ArgumentParser()
required_flags = parser.add_argument_group(title="Required")
required_flags.add_argument("--datafile",required=True,  help="JSON filepath to read", type=str)
required_flags.add_argument("--output", required=True, help="JSON filepath to output vision collission matrices", type=str)
parser.add_argument("--show", help="Show output map and ship locations", action="store_true")
args = parser.parse_args()


data_filepath = args.datafile

# Reads the json data
received_data = aux.JSON_to_dict(data_filepath)


# Processes the obstacles
obstacles = received_data["obstacles"]
circle_obstacles_in_map = []
polygon_obstacles_in_map = []

for an_obstacle in obstacles:

    # Generates circle
    if an_obstacle["type"] == "circle":
        circle_obstacles_in_map.append(aux.Circle_obstacle(an_obstacle["center"], an_obstacle["r"]))

    elif an_obstacle["type"] == "polygon":
        polygon_obstacles_in_map.append(aux.Polygon_obstacle(an_obstacle["points"]))


# Obtains the positions
positions = received_data["positions"]

# Obtains the x coordinate, y coordinate, angle (radians, CCW, starting at 3:00), and action code
player_x, player_y, angles, action_codes = [], [], [], []
num_positions = len(positions)


# Total obstacles
total_obstacles = circle_obstacles_in_map + polygon_obstacles_in_map


for a_position in positions:

    xc, yc = a_position[0]

    # Ensures that the point does not collide with any obstacle
    for an_obstacle in total_obstacles:
        assert not an_obstacle.collides_with([xc, yc]), "Point %f, %f collides with an obstacle"

    player_x.append(xc)
    player_y.append(yc)
    angles.append(a_position[1])

    assert a_position[2] in [0, 1, 2, 3], "Action code should be 0, 1, 2, 3; it currently is " + str(a_position[2])

    action_codes.append(a_position[2])


# Generates the matrix of vectors to check around the ship

# Number of divisions, must be odd to ensure [0, 0] (ship's position) is present
divisions_x = 41
divisions_y = 41

checks_x = np.linspace(-10, 10, divisions_x)
checks_y = np.linspace(-10, 10, divisions_y)


checks_V = [[[] for j in range(0, divisions_y)] for i in range(0, divisions_x)]

for xpos in range(0, divisions_x):
    for ypos in range(0, divisions_y):
        checks_V[xpos][ypos] = [checks_x[xpos], checks_y[ypos]]



# Generates the map, which is always a polygon
circuit_points = received_data["circuit"]
circuit_polygon = aux.Polygon_obstacle(circuit_points)




# For each point, it calculates the output matrix
# The matrix only checks one point in particular
# 1: Empty
# 0: Blocked by some object
collision_data = []
for i in range(0, num_positions):

    current_collision_matrix = aux.compute_collision_matrix(checks_V, total_obstacles, player_x[i], player_y[i], angles[i], divisions_x, divisions_y, circuit_polygon)
    collision_data.append(current_collision_matrix)




# Stores the data in JSON
output_data = {"metadata":received_data["metadata"], "collisions":collision_data}

with open(args.output, "w") as jf:
    jf.write(json.dumps(output_data, indent=4))



# Notifies server
# TODO



# If show, show the resultant map
if args.show:

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot the circle borders
    ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], "k-")


    # Shows the map
    cx, cy = [], []

    for a_point in circuit_polygon.points:
        cx.append(a_point[0])
        cy.append(a_point[1])

    ax.fill(cx, cy, color="grey", alpha=0.5)


    # Shows the circle obstacles
    for a_co in circle_obstacles_in_map:
        tmp = plt.Circle((a_co.cx, a_co.cy), a_co.r, color="gold", clip_on=True )
        ax.add_patch(tmp)

    # Shows the polygon obstacles
    for a_pol in polygon_obstacles_in_map:

        x, y = [], []

        for a_point in a_pol.points:
            x.append(a_point[0])
            y.append(a_point[1])

        ax.fill(x, y, color="gold")


    # Shows the player locations
    ax.plot(player_x, player_y, "bo-")


    # Shows arrows indicating where the boat is pointing at this instant (before the action is taken)
    for i in range(0, num_positions):
        plt.arrow(player_x[i], player_y[i], math.cos(angles[i]), math.sin(angles[i]), head_width=0.8) 


    # Shows the map



    # Shows the map
    plt.xlim([-1, 101])
    plt.ylim([-1, 101])
    plt.show()
