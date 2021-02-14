"""
SUMMARY

Auxiliary functions for preprocessor.py, added here to avoid clutter.
"""

import json
import sys


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



