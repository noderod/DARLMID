"""
SUMMARY

A* trainer from a Q matrix, designed to help a Q learning agent.
"""

import argparse
from heapq import *
import json
import random
import sys

import matplotlib.pyplot as plt

import auxiliary as aux
from vehicle import Vehicle


# Sets seed for reproducibility
random.seed(0)



# Processes arguments
parser = argparse.ArgumentParser()
required_flags = parser.add_argument_group(title="Required")
required_flags.add_argument("--A-star-runs",required=True,  help="Number of A* runs", type=int)
required_flags.add_argument("--data",required=True,  help="JSON filepath to read Q, rewards matrices and other information", type=str)
required_flags.add_argument("--output", required=True, help="JSON filepath to output the results", type=str)
args = parser.parse_args()


assert args.A_star_runs > 1, "There must be at least one A* run"


#-----------------------------------------------------
# DATA PREPROCESSING
#-----------------------------------------------------

# Loads original data
with open(args.data, "r") as jf:
    original_data =  json.load(jf)

R = original_data["rewards matrix"]
Q = original_data["Q matrix"]

nx = original_data["nx"]
ny = original_data["ny"]
goal_discrete_loc = original_data["goal discrete location"]
possible_speeds = original_data["possible speeds"]
speed_max = possible_speeds - 1

valid_positions = original_data["valid positions"]
num_valid_positions = len(valid_positions)

orientations = [i for i in range(0, len(original_data["orientations"]))]
actions = [j for j in range(0, len(original_data["actions"]))]


# Calculates all the L1 distances
L1_distance_to_goal_matrix = [[0 for y in range(0, ny)] for x in range(0, nx)]
for x in range(0, nx):
    for y in range(0, ny):
        L1_distance_to_goal_matrix[x][y] = aux.L1([x, y], goal_discrete_loc)



#-----------------------------------------------------
# FUNCTIONS
#-----------------------------------------------------

# Generates a string ("[x, y, o, v]") representing the state (s)
def generate_sa_str(x, y, o, v):
    return "%d, %d, %d, %d" % (x, y, o, v)


# Retrieves s from the "[x, y, o, v]" string
def retrieve_sa_from_str(sa_str):

    vars_only = sa_str.split(", ")
    vars_as_int = [int(var) for var in vars_only]

    return vars_as_int


# Executes a single A* search
def A_star_search():

    #Starts in a random location with random orientation and always 0 speed
    starting_location = valid_positions[random.randint(0, num_valid_positions-1)]
    starting_orientation = random.randint(0, 3)

    # The heap has elements: (L1 distance, [s, a] string)
    heap_tracker = []
    # Adds the first element
    starting_sa = generate_sa_str(starting_location[0], starting_location[1], starting_orientation, 0)
    heappush(heap_tracker, (aux.L1(starting_location, goal_discrete_loc),
            starting_sa)
    )

    # Keeps track of already visited spaces and actions
    # {"[x, y, o, v]":[previous state, action taken]}
    already_visited_sa = {}
    already_visited_sa[starting_sa] = [None, None]

    # Keep going while there are elements in the priority queue
    goal_not_reached = True
    while (len(heap_tracker) != 0) and (goal_not_reached):

        # Gets the first element in the list (as state str)
        # 1 because 0 would be the L1 distance
        s_previous = heappop(heap_tracker)[1]

        # Gets its variables
        [s_x, s_y, s_o, s_v] = retrieve_sa_from_str(s_previous)

        # Explore using all possible actions
        for action_index in range(0, 5):

            # Creates a vehicle and executes the action, obtaining the end state
            one_action_vehicle = Vehicle(nx, ny, s_x, s_y, s_o, s_v, speed_max, R)
            [_1, location_end] = one_action_vehicle.execute_action(action_index,
                                                                    modify_self=False,
                                                                    get_copy_there=False,
                                                                    get_end_location=True)

            v_x_new = location_end[0][0]
            v_y_new = location_end[0][1]
            v_orientation_new = location_end[1]
            v_speed_new = location_end[2]

            s_new = generate_sa_str(v_x_new, v_y_new, v_orientation_new, v_speed_new)

            # If already seen this state, skip
            if s_new in already_visited_sa:
                continue

            # Get L1 to this new state
            L1_to_goal_from_here = aux.L1(location_end[0], goal_discrete_loc)
            # Add to heap
            heappush(heap_tracker, (L1_to_goal_from_here, s_new))
            # Adds to the dictionary as already visited
            already_visited_sa[s_new] = [s_previous, action_index]

            # If this point is the goal (L1 = 0), then stop here
            if L1_to_goal_from_here == 0:
                goal_not_reached = False
                goal_state = s_new
                break


    # Retraces steps from the goal
    # [[x, y, o, v, a]]
    steps_from_goal = []
    current_state = goal_state
    while already_visited_sa[current_state] != [None, None]:

        # Gets the previous state and action
        state_p, action_p = already_visited_sa[current_state]

        [x_p, y_p, o_p, v_p] = retrieve_sa_from_str(state_p)
        steps_from_goal.append([x_p, y_p, o_p, v_p, action_p])

        # Current state becomes the previous state
        current_state = state_p


    # Returns the steps inverted
    return steps_from_goal[::-1]





#-----------------------------------------------------
# A*
#-----------------------------------------------------


actions_taken = []


for a_run in range(0, args.A_star_runs):
    actions_taken.append(A_star_search())



#-----------------------------------------------------
# SAVES THE OUTPUT
#-----------------------------------------------------

with open(args.output, "w") as jf:
    jf.write(json.dumps({"actions taken":actions_taken, "intent":"positive"}, indent=4))

