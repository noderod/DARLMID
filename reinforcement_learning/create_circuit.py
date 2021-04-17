"""
SUMMARY

Generates a Q-matrix of circuit based on a template
Shows the circuit if requested
"""


import argparse
import json

import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

import auxiliary as aux


# Processes arguments
parser = argparse.ArgumentParser()
required_flags = parser.add_argument_group(title="Required")
required_flags.add_argument("--circuit",required=True,  help="JSON filepath to read circuit information from", type=str)
required_flags.add_argument("--output", required=True, help="JSON filepath to output Q matrix and other data", type=str)
parser.add_argument("--show", help="Show output map and ship locations", action="store_true")
args = parser.parse_args()


#---------------------------------------
# DATA PREPROCESSING
#---------------------------------------

# Loads all the circuit data
circuit_filepath = args.circuit

with open(circuit_filepath, "r") as jf:
    original_data =  json.load(jf)


# X coordinate discretization
nx = original_data["nx"]
# Y coordinate discretization
ny = original_data["ny"]

# Circuit points
original_circuit_points = original_data["circuit"]
# Obstacles (only take one element when discretized)
obstacles = original_data["obstacles"]


# Generates the appropiate shapely polygon
circuit_shapely = Polygon([(p[0], p[1]) for p in original_circuit_points])

# Obtains the bounds
[x_min, y_min, x_max, y_max] = circuit_shapely.bounds
loc_min = [x_min, y_min]

x_interval = x_max - x_min
y_interval = y_max - y_min

Δx = x_interval/nx
Δy = y_interval/ny
Δxy = [Δx, Δy]


# Gets the range of velocities (including zero)
possible_speeds = original_data["speed range"]
assert possible_speeds > 1, "There must be at least one speed apart from zero"

# Goal location
goal_location = original_data["goal"]


#---------------------------------------
# GENERATING THE REWARDS MATRIX
#---------------------------------------

# Rewards matrix, empty as of now
# All points are -1 by default
R = [[0 for yloc in range(0, ny)] for xloc in range(0, nx)]


# Goes through every point in the range, sets it as -1 (default) if within circuit, -100 if not (outside, crash if reached)
for xloc in range(0, nx):
    for yloc in range(0, ny):

        [xc, yc] = aux.continuous_location([xloc, yloc], loc_min, Δxy)
        xc_shapely_point = Point((xc, yc))

        if circuit_shapely.intersects(xc_shapely_point) or circuit_shapely.contains(xc_shapely_point):
            R[xloc][yloc] = -1
        else:
            R[xloc][yloc] = -100


# Obstacle locations are marked as -100 (crash)
for an_obstacle in obstacles:
    [obs_xd, obs_yd] = aux.discretize_location(an_obstacle, loc_min, Δxy)
    R[obs_xd][obs_yd] = -100


# Goal location provides a +100 reward
goal_discrete_loc = aux.discretize_location(goal_location, loc_min, Δxy)
R[goal_discrete_loc[0]][goal_discrete_loc[1]] = 100


# Gets a list of all valid intermediate locations (inside the circuit, not an obstacle, not the goal location)
valid_position = []

for xloc in range(0, nx):
    for yloc in range(0, ny):

        if R[xloc][yloc] == -1:
            valid_position.append([xloc, yloc])


#---------------------------------------
# GENERATING THE Q REWARDS MATRIX
#---------------------------------------



# Empty matrix








#---------------------------------------
# SHOWS THE CORRESPONDING CIRCUIT
#---------------------------------------

plt.figure()

# Intermediate locations shown in light blue
for a_valid_position in valid_position:
    valid_cell_discrete_to_continuous = aux.continuous_location(a_valid_position, loc_min, Δxy)
    cell_borders = aux.cell_borders(valid_cell_discrete_to_continuous, Δxy)
    plt.fill(cell_borders[0], cell_borders[1], color="gainsboro")
    # Shows the borders
    plt.plot(aux.first_append_to_last(cell_borders[0]), aux.first_append_to_last(cell_borders[1]), "k-")


# Goal location shown in green

# Bottom left of goal cell
goal_cell_discrete_to_continuous = aux.continuous_location(goal_discrete_loc, loc_min, Δxy)
goal_borders = aux.cell_borders(goal_cell_discrete_to_continuous, Δxy)
plt.fill(goal_borders[0], goal_borders[1], color="yellowgreen")
# Shows the border
plt.plot(aux.first_append_to_last(goal_borders[0]), aux.first_append_to_last(goal_borders[1]), "k-")

plt.show()
