"""
SUMMARY

Allows to compare the rewards and Q matrices (in the form of a heatmap) between Q learning agents.
Modify the file names and plotting variables accordingly
Both Q1 and Q2 must have the same dimensions, but not the rewards and epochs
"""


import json

import matplotlib.pyplot as plt


# File names
q1_file = "results/five_output.json"
q2_file = "results/five_positive_and_negative_output.json"

# Plotting variables
q1_label = "Standard Q-learning"
q2_label = "Combined demonstrations"

#-----------------------------------------------------
# DATA PREPROCESSING
#-----------------------------------------------------

# Loads Q1 data
with open(q1_file, "r") as jf:
    q1_data = json.load(jf)
    Q1 = q1_data["Q matrix"]
    q1_epoch_rewards = q1_data["epoch rewards"]

# Loads Q2 data
with open(q2_file, "r") as jf:
    q2_data = json.load(jf)
    Q2 = q2_data["Q matrix"]
    q2_epoch_rewards = q2_data["epoch rewards"]


# Calculates the summarized Q matrix by calculating the average of each x, y value (averaging over orientations, speeds, and actions)
# This is done since the heatmap would be 2D only
nx = len(Q1)
ny = len(Q1[0])

averaged_difference_sq = [[0 for y in range(0, ny)] for x in range(0, nx)]

num_orientations = len(Q1[0][0])
num_speeds = len(Q1[0][0][0])
num_actions = 5

# o*v*a
n = num_orientations*num_speeds*num_actions

for x in range(0, nx):
    for y in range(0, ny):

        Q1_xy = Q1[x][y]
        Q2_xy = Q2[x][y]

        q1_var = 0
        q2_var = 0

        for an_orientation in range(0, num_orientations):
            for a_speed in range(0, num_speeds):
                q1_var += sum(Q1_xy[an_orientation][a_speed])
                q2_var += sum(Q2_xy[an_orientation][a_speed])

        averaged_difference_sq[x][y] = ((q1_var/n) - (q2_var/n))**2


# Gets the epoch rewards into two arrays (epoch and rewards) for plotting
q1_epochs, q2_epochs = [], []
q1_rewards, q2_rewards = [], []

for an_er in q1_epoch_rewards:
    q1_epochs.append(an_er[0])
    q1_rewards.append(an_er[1])

for an_er in q2_epoch_rewards:
    q2_epochs.append(an_er[0])
    q2_rewards.append(an_er[1])


#-----------------------------------------------------
# PLOTS EPOCH REWARDS
#-----------------------------------------------------

plt.figure(0)

plt.plot(q1_epochs, q1_rewards, "r-", label=q1_label)
plt.plot(q2_epochs, q2_rewards, "g-", label=q2_label)

plt.xlabel("Epochs")
plt.ylabel("Averaged reward")
plt.legend()

plt.title("%s vs %s" % (q1_label, q2_label))


#-----------------------------------------------------
# PLOTS HEATMAP DIFFERENCES
#-----------------------------------------------------

plt.figure(1)
plt.imshow(averaged_difference_sq, cmap="jet", interpolation="nearest", origin="lower")
plt.colorbar()
plt.title("Squared average difference per Q[s=(x, y)] cell")




#-----------------------------------------------------
# SHOWS PLOTS
#-----------------------------------------------------

plt.show()
