"""
BASICS

Creates the necessary tables and users.
"""

import os


import psycopg2

con = psycopg2.connect (host = os.environ["POSTGRES_URL"], database = os.environ["POSTGRES_DB"], user = os.environ["POSTGRES_USER"], password = os.environ["POSTGRES_PASSWORD"])
cur = con.cursor()


# Creates main user table
cur.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    user_id        serial PRIMARY KEY,
    username       VARCHAR (256) UNIQUE NOT NULL,
    password       VARCHAR (256) NOT NULL,
    salt           VARCHAR (256) NOT NULL,
    date_creation  TIMESTAMP NOT NULL,
    last_action    TIMESTAMP NOT NULL,
    last_login     TIMESTAMP NOT NULL,
    last_logout    TIMESTAMP NOT NULL
)""")


# Creates a read only user (SELECT)
# Query is done in an unsafe way because it is the only way, sanitizing it will cause issues
# No user input
read_only_postgres_user = os.environ["R_USERNAME"]
cur.execute("CREATE USER "+ read_only_postgres_user + " WITH ENCRYPTED PASSWORD %s", (os.environ["R_PASSWORD"],))
cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO " + read_only_postgres_user)


# Creates a write user (SELECT, INSERT, UPDATE)
write_postgres_user = os.environ["RW_USERNAME"]
cur.execute("CREATE USER "+ write_postgres_user + " WITH ENCRYPTED PASSWORD %s", (os.environ["RW_PASSWORD"],))
cur.execute("GRANT SELECT, INSERT, DELETE, UPDATE ON ALL TABLES IN SCHEMA public TO " + write_postgres_user)
cur.execute("GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO " + write_postgres_user)


con.commit()
con.close ()
