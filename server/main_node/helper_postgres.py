"""
BASICS

Auxiliary functions for traffic.py for the PostgreSQL database only
"""

import datetime
import hashlib
import os
import random

import psycopg2



"""
Checks if a username is in the database. -> Boolean

given_username (str)
"""
def username_in_db(given_username):

    con = psycopg2.connect (host = os.environ["POSTGRES_URL"], database = os.environ["POSTGRES_DB"], user = os.environ["R_USERNAME"], password = os.environ["R_PASSWORD"])
    cur = con.cursor()

    # Creates main user table
    cur.execute("SELECT username FROM user_data WHERE username=%s", (given_username,))

    found_username = (cur.fetchone() != None)
    con.close()

    return found_username



"""
Creates a unique salt. -> str
"""
def generate_salt():
    return hashlib.sha512(str(random.random()).encode("utf-8")).hexdigest()



"""
Obtains the UTC time now. -> datetime
"""
def get_UTC_time():
    return datetime.datetime.utcnow()

"""
Salts a given password -> str
"""
def salt_password(password, salt):
    return hashlib.sha512((password + salt).encode("utf-8")).hexdigest()



"""
Generates a new user.
Assumed that the user is not already there.

given_username (str)
given_password (str)
"""
def create_new_user(given_username, given_password):

    con = psycopg2.connect (host = os.environ["POSTGRES_URL"], database = os.environ["POSTGRES_DB"], user = os.environ["RW_USERNAME"], password = os.environ["RW_PASSWORD"])
    cur = con.cursor()

    salt = generate_salt()

    current_UTC_time = get_UTC_time()

    # Inserts the user in the appropriate table
    cur.execute("INSERT INTO user_data(username, password, salt, date_creation, last_action, last_login, last_logout) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (given_username, salt_password(given_password, salt), salt, current_UTC_time, current_UTC_time, current_UTC_time, current_UTC_time))

    con.commit()
    con.close()



"""
Checks if a username and password (after salted and hashed) are in the database. -> Boolean

given_username (str): Assumed to exist (must be checked before)
given_password (str): Unsalted
"""
def verify_username_password(given_username, given_password):

    con = psycopg2.connect (host = os.environ["POSTGRES_URL"], database = os.environ["POSTGRES_DB"], user = os.environ["R_USERNAME"], password = os.environ["R_PASSWORD"])
    cur = con.cursor()

    # Obtains the salt
    cur.execute("SELECT salt, password FROM user_data WHERE username=%s", (given_username,))

    obtained_result = cur.fetchone()

    con.close()


    if obtained_result == None:
        return False

    salt, stored_salted_password = obtained_result
    salted_password = salt_password(given_password, salt)

    return stored_salted_password == salted_password
