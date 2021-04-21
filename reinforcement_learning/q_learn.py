"""
SUMMARY

Reinforcement learning via q-learning on the provided data, using previous data if requested
"""

import argparse
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
required_flags.add_argument("--epochs",required=True,  help="Number of epochs", type=int)
required_flags.add_argument("--explore-probability",required=True,  help="Explore probability [0, 1]", type=float)
required_flags.add_argument("--learning-rate",required=True,  help="Learning rate [0, 1]", type=float)
required_flags.add_argument("--discount-factor",required=True,  help="Discount factor [0, 1]", type=float)
required_flags.add_argument("--data",required=True,  help="JSON filepath to read Q, rewards matrices and other information", type=str)
required_flags.add_argument("--positive-demonstration", help="JSON filepath to read Q matrix updates after a number of positive demonstrations (already processed)", type=str)
required_flags.add_argument("--negative-demonstration", help="JSON filepath to read Q matrix updates after a number of negative demonstrations (already processed)", type=str)
required_flags.add_argument("--good-advice-decay", help="Training epochs good advice is remembered (50 by defaulr)", type=int)
required_flags.add_argument("--bad-advice-decay", help="Training epochs bad advice is remembered (5 by defaulr)", type=int)
required_flags.add_argument("--output", required=True, help="JSON filepath to output the results", type=str)
parser.add_argument("--show", help="Show output reward vs. epoch plot", action="store_true")
args = parser.parse_args()


p_exp = args.explore_probability
α = args.learning_rate
γ = args.discount_factor

assert (0 <= p_exp) and (p_exp <= 1), "Explore probability must be between 0 and 1"
assert (0 <= α) and (α <= 1), "Learning rate must be between 0 and 1"
assert (0 <= γ) and (γ <= 1), "Discount factor must be between 0 and 1"


good_advice_decay_epochs = 50
bad_advice_decay_epochs = 5

if args.good_advice_decay:
    assert args.good_advice_decay >= 0, "Good advice decay cannot be negative epochs"
    good_advice_retention_epochs = args.good_advice_decay

if args.bad_advice_decay:
    assert args.bad_advice_decay >= 0, "Bad advice decay cannot be negative epochs"
    bad_advice_retention_epochs = args.bad_advice_decay



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

# Stores advice actions
# "good":{"x, y, o, v":True, ...}
# "bad": {"x, y, o, v":True, ...}
advice_locations = {"good":{}, "bad":{}}

# From Useful Policy Invariant Shaping from Arbitrary Advice (Behboudian et al.)



# Utilizes positive demonstration data
# Positive intent -> Intentionally good demonstrations (although perhaps the user is incompetent)
if args.positive_demonstration:

    # Retrieves demonstration data
    with open(args.positive_demonstration, "r") as jf:
        original_demonstration_data =  json.load(jf)

    action_sets_taken = original_demonstration_data["actions taken"]

    # Simply take the data as is, modify the appropriate Q matrix value, adding +1 to the appropiate Q[s, a] location
    for an_action_path in action_sets_taken:

        # Goes step by step
        for a_step in an_action_path:
            step_x = a_step[0]
            step_y = a_step[1]
            step_o = a_step[2]
            step_v = a_step[3]
            step_a = a_step[4]

            Q[step_x][step_y][step_o][step_v][step_a] += 1
            advice_locations["good"][aux.state_to_str(step_x, step_y, step_o, step_v)] = good_advice_decay_epochs


# Utilizes negative demonstration data
# Negative intent -> Intentionally poor or misleading demonstrations
if args.negative_demonstration:

    # Retrieves demonstration data
    with open(args.negative_demonstration, "r") as jf:
        original_demonstration_data =  json.load(jf)

    action_sets_taken = original_demonstration_data["actions taken"]

    for an_action_path in action_sets_taken:

        # Goes step by step
        for a_step in an_action_path:
            step_x = a_step[0]
            step_y = a_step[1]
            step_o = a_step[2]
            step_v = a_step[3]
            step_a = a_step[4]

            # Desincentive bad behaviour in the Q matrix
            Q[step_x][step_y][step_o][step_v][step_a] -= 1
            advice_locations["bad"][aux.state_to_str(step_x, step_y, step_o, step_v)] = bad_advice_decay_epochs



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

    # Stores the good and bad advice states reached this round
    good_advice_states_seen = {}
    bad_advice_states_seen = {}

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

            # Only modifies the current value if the advice memory has not run out yet in general
            s_as_state = aux.state_to_str(v_x, v_y, v_orientation, v_speed)

            if (s_as_state in advice_locations["good"]) and (advice_locations["good"][s_as_state] > 0):

                if s_as_state not in good_advice_states_seen:
                    good_advice_states_seen[s_as_state] = True
                continue
            elif (s_as_state in advice_locations["bad"]) and (advice_locations["bad"][s_as_state] > 0):

                if s_as_state not in bad_advice_states_seen:
                    bad_advice_states_seen[s_as_state] = True
                continue

            Q[v_x][v_y][v_orientation][v_speed][chosen_action_index] = Q_sa + α*(R[v_x][v_y] + γ*Q_apostrophe_max - Q_sa)


    # Marks certain states as seen this round
    for a_good_seen_state in good_advice_states_seen:
        # Good advice reward decays
        advice_locations["good"][a_good_seen_state] -= 1/good_advice_decay_epochs

    for a_bad_seen_state in bad_advice_states_seen:
        # Bad advice reward rises
        advice_locations["bad"][a_bad_seen_state] += 1/bad_advice_decay_epochs



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
