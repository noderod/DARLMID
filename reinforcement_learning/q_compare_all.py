"""
SUMMARY

Allows to compare the rewards among all the provided data files
Modify the file names and plotting variables accordingly
Both Q1 and Q2 must have the same dimensions, but not the rewards and epochs
"""


import json

import matplotlib.pyplot as plt


output_files = ["results/five_output.json", "results/five_A_1_output.json", "results/five_negative_output.json", "results/five_positive_output.json", "results/five_positive_and_negative_output.json"]
output_labels = ["Standard Q-learning", "A* demonstrations", "Negative demonstrations", "Positive demonstrations", "Combined demonstrations"]
output_colors = ["k", "b", "r", "g", "m"]


plt.figure(0)

for nv in range(0, len(output_files)):

    with open(output_files[nv], "r") as jf:
        reward_epochs = json.load(jf)["epoch rewards"]

    epochs = []
    rewards = []

    for an_er in reward_epochs:
        epochs.append(an_er[0])
        rewards.append(an_er[1])

    plt.plot(epochs, rewards, ls="-", color=output_colors[nv], label=output_labels[nv], lw=3)



plt.xlabel("Epochs")
plt.ylabel("Averaged reward")
plt.legend()

plt.title("Reward vs Epoch")




#-----------------------------------------------------
# SHOWS PLOTS
#-----------------------------------------------------

plt.show()
