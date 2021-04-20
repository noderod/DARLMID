#!/bin/bash

# Sleeps for 10 s so that the PostgreSQL is ready
sleep 10

# Creates the necessary tables
python3 create_tables.py

# Sets up the APIs
gunicorn traffic:DARLMID_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5


# Sleeps forever
# Added in case one of the above commands needs to be killed
sleep infinity
