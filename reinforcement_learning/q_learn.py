"""
SUMMARY

Reinfrocement learning via q-learning on the provided data, using previous data if requested
"""

import argparse
import json
import random
import sys

import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

import auxiliary as aux
from vehicle import Vehicle


# Sets seed for reproducibility
random.seed(0)



# Processes arguments
parser = argparse.ArgumentParser()
required_flags = parser.add_argument_group(title="Required")
required_flags.add_argument("--epochs",required=True,  help="Number of epochs", type=int)
required_flags.add_argument("--explore-probability",required=True,  help="Explore probability [0, 1]", type=float)
required_flags.add_argument("--learning-rate",required=True,  help="Learning rate [0, 1]", type=float)
required_flags.add_argument("--discount-factor",required=True,  help="Discount factor [0, 1]", type=float)
required_flags.add_argument("--data",required=True,  help="JSON filepath to read Q, rewards matrices and other information", type=str)
required_flags.add_argument("--demonstration", help="JSON filepath to read Q matrix updates after a number of demonstrations (already processed)", type=str)
required_flags.add_argument("--output", required=True, help="JSON filepath to output the results", type=str)
parser.add_argument("--show", help="Show output reward vs. epoch plot", action="store_true")
args = parser.parse_args()


p_exp = args.explore_probability
α = args.learning_rate
γ = args.discount_factor

assert (0 <= p_exp) and (p_exp <= 1), "Explore probability must be between 0 and 1"
assert (0 <= α) and (α <= 1), "Learning rate must be between 0 and 1"
assert (0 <= γ) and (γ <= 1), "Discount factor must be between 0 and 1"



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
possible_speeds = original_data["possible speeds"]
speed_max = possible_speeds - 1

valid_positions = original_data["valid positions"]

orientations = [i for i in range(0, len(original_data["orientations"]))]
actions = [j for j in range(0, len(original_data["actions"]))]



#-----------------------------------------------------
# UPDATES Q MATRIX WITH DEMONSTRATION RESULTS
#-----------------------------------------------------

# TODO



#-----------------------------------------------------
# NECESSARY FUNCTIONS
#-----------------------------------------------------



# Tests with the current Q matrix
# Each epoch tests a starting location with a random orientation but always zero speed
# Each reward in the array is: max(Reward - steps, 0)
# Up to 100 steps can be used
# Returns an array containing rewards
max_testing_iterations = 100
def test_Q():

    results = []

    # Reshuffles the valid starting locations
    random.shuffle(valid_positions)

    # Goes through every valid position
    for a_valid_position in valid_positions:
        xloc, yloc = a_valid_position
        starting_orientation = random.randint(0, 3)
        tested_vehicle = Vehicle(nx, ny, xloc, yloc, starting_orientation, 0, speed_max, R)

        reward_so_far = 0

        for an_iteration in range(0, max_testing_iterations):

            # Gets the current location
            v_x = tested_vehicle.xloc
            v_y = tested_vehicle.yloc
            v_orientation = tested_vehicle.orientation_index
            v_speed = tested_vehicle.speed

            # Adds the penalty/reward corresponding to this location
            reward_so_far += R[v_x][v_y]

            # If this is a reward, obstacle, or outside the circuit (unless it is outside the borders) add the reward and then exit this iteration
            if R[v_x][v_y] != -1:
                break

            # Chooses the action index with the maximum reward in Q
            # If two actions have the same optimal Q-value, the first one will be chosen
            Q_values_to_choose = Q[v_x][v_y][v_orientation][v_speed]
            best_Q_value = max(Q_values_to_choose)
            action_index = Q_values_to_choose.index(best_Q_value)

            # Makes the vehicle attempt it
            tested_vehicle.execute_action(action_index, modify_self=True, get_copy_there=False, get_end_location=False)

        results.append(max(0, reward_so_far))

    return results



# Trains starting with the current Q matrix, which is updated at each step
# Each epoch tests a starting location with a random orientation but always zero speed
# Each reward in the array is: max(Reward - steps, 0)
# Up to 100 steps can be used
# Does not return anything
max_training_iterations = 100
def train_Q():

    # Reshuffles the valid starting locations
    random.shuffle(valid_positions)

    # Goes through every valid position
    for a_valid_position in valid_positions:
        xloc, yloc = a_valid_position
        starting_orientation = random.randint(0, 3)
        tested_vehicle = Vehicle(nx, ny, xloc, yloc, starting_orientation, 0, speed_max, R)

        for an_iteration in range(0, max_training_iterations):

            # Gets the current location
            v_x = tested_vehicle.xloc
            v_y = tested_vehicle.yloc
            v_orientation = tested_vehicle.orientation_index
            v_speed = tested_vehicle.speed

            # If this is a reward, obstacle, or outside the circuit (unless it is outside the borders) then exit this iteration
            if R[v_x][v_y] != -1:
                break

            # Gets a random probability
            what_to_do = random.random()

            # If below the explore probability, explore, choose an action at random
            if what_to_do <= p_exp:
                chosen_action_index = random.randint(0, 4)
            else:
                # Chooses the action index with the maximum reward in Q
                # If two actions have the same optimal Q-value, the first one will be chosen
                Q_values_to_choose = Q[v_x][v_y][v_orientation][v_speed]
                best_Q_value = max(Q_values_to_choose)
                chosen_action_index = Q_values_to_choose.index(best_Q_value)

            # Makes the vehicle attempt the action
            [_1, location_end] = tested_vehicle.execute_action(chosen_action_index,
                                                                modify_self=True,
                                                                get_copy_there=False,
                                                                get_end_location=True)

            # Updates the Q matrix
            # Q[s, a] = Q[s, a] + α*(R[s] + γ*max(Q[s', a'], a') - Q[s, a])

            v_x_new = location_end[0][0]
            v_y_new = location_end[0][1]
            v_orientation_new = location_end[1]
            v_speed_new = location_end[2]

            Q_apostrophe_max = max(Q[v_x_new][v_y_new][v_orientation_new][v_speed_new])
            Q_sa = Q[v_x][v_y][v_orientation][v_speed][chosen_action_index]

            Q[v_x][v_y][v_orientation][v_speed][chosen_action_index] = Q_sa + α*(R[v_x][v_y] + γ*Q_apostrophe_max - Q_sa)



#-----------------------------------------------------
# Q-LEARNING
#-----------------------------------------------------

# [[epoch index, RMS reward], ...]
epoch_rewards = []

for an_epoch in range(0, args.epochs):

    # Tests
    tested_rewards = test_Q()

    # Calculates and appends the RMS reward to results
    epoch_rewards.append([an_epoch, aux.RMS(tested_rewards)])

    # Trains (unless it is the last epoch)
    if an_epoch != (args.epochs - 1):
        train_Q()


#-----------------------------------------------------
# OUTPUTS RESULTS
#-----------------------------------------------------

with open(args.output, "w") as jf:
    jf.write(json.dumps({"Q matrix":Q, "epoch rewards":epoch_rewards}, indent=4))



#-----------------------------------------------------
# SHOWS PLOT WITH RESULTS IF REQUESTED
#-----------------------------------------------------

if not args.show:
    sys.exit()

plt.figure()


epochs_used = []
rewards_obtained = []

for mt in range(0, len(epoch_rewards)):
    epochs_used.append(epoch_rewards[mt][0])
    rewards_obtained.append(epoch_rewards[mt][1])

plt.plot(epochs_used, rewards_obtained, "k-")

plt.xlabel("Epoch")
plt.ylabel("Reward")
plt.title("Reward vs. Epoch")

plt.show()
