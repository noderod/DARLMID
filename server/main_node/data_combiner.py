"""
SUMMARY

Combines positive and negative demonstration data into a form usable by reinforcement-learning/q_learn.py
"""

import os
import json

positive_intent_location = "/DARLMID/data/positive/"
negative_intent_location = "/DARLMID/data/negative/"


positive_intent_data = {"intent":"positive", "actions taken":[]}
negative_intent_data = {"intent":"negative", "actions taken":[]}


# Reads the positive data
for a_positive_file in os.listdir(positive_intent_location):

    full_path_file = positive_intent_location + a_positive_file

    with open(full_path_file, "r") as jf:
        positive_data = json.load(jf)

    positive_intent_data["actions taken"].append(positive_data["actions taken"])

# Writes the positive data
with open("/DARLMID/data/combined_positive.json", "w") as wf:
    wf.write(json.dumps(positive_intent_data, indent=4))


# Reads the negative data
for a_negative_file in os.listdir(negative_intent_location):

    full_path_file = negative_intent_location + a_negative_file

    with open(full_path_file, "r") as jf:
        negative_data = json.load(jf)

    negative_intent_data["actions taken"].append(negative_data["actions taken"])

# Writes the negative data
with open("/DARLMID/data/combined_negative.json", "w") as wf:
    wf.write(json.dumps(negative_intent_data, indent=4))
