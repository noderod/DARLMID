"""
SUMMARY

Pre-processes a JSON file obtained from the server, verifying that all the information is there.
Then, it creates a map and tracks the movements and actions there.
It produces another JSON file with a series of matrices composed of 0 and 1, representing whether or not a certain location is occupied
by an object or outside the map
"""

import argparse
import json

import shapely

import aux



# Processes arguments
parser = argparse.ArgumentParser()
parser.add_argument("--datafile", help="JSON filepath to read", type=str)
parser.add_argument("--show", help="Show output map and ship locations")
args = parser.parse_args()


data_filepath = args.datafile

# Reads the json data
received_news = aux.JSON_to_dict(data_filepath)










# If show, show the resultant map
