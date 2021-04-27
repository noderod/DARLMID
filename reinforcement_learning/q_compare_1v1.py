"""
SUMMARY

Allows to compare the rewards between Q learning agents.
Modify the file names and plotting variables accordingly
Both Q1 and Q2 must have the same dimensions, but not the rewards and epochs
"""


import json

import matplotlib.pyplot as plt


# File names
q1_file = "results/five_output.json"
q2_file = "results/five_negative_output.json"

# Plotting variables
q1_label = "Standard Q-learning"
q2_label = "Combined positive and negative demonstrations"

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
# SHOWS PLOTS
#-----------------------------------------------------

plt.show()
