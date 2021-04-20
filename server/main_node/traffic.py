"""
SUMMARY

Directs TCP traffic and executes the appropriate commands or returning the correct file
"""

import json
import os
import uuid

from aiohttp import web

from helper import *
from helper_postgres import *


# Checks if the user is logged-in via cookie
async def is_logged_in(request):
    if "DARLMID_key" not in request.cookies:
        return False
    else:
        # Verify the key's contents
        DARLMID_key = request.cookies["DARLMID_key"]
        return await verify_cookie_key(DARLMID_key)




# Serves Index (main HTML file)
async def index(request):

    if await is_logged_in(request):
        return web.FileResponse('/DARLMID/html/index_logged_in.html')

    # Non-logged-in index
    return web.FileResponse('/DARLMID/html/index.html')


# Serves the driving page to train the driving agent based on demonstrations
async def driving(request):

    if await is_logged_in(request):
        return web.FileResponse('/DARLMID/html/driving.html')

    # Non-logged-in index
    raise web.HTTPFound("/")



# Sign-Up page
async def sign_up(request):

    # Logged-in, redirect to /
    if await is_logged_in(request):
        raise web.HTTPFound("/")

    # Non-logged-in sign-up
    return web.FileResponse('/DARLMID/html/sign_up.html')


# Login page
async def login(request):

    # Logged-in, redirect to /
    if await is_logged_in(request):
        raise web.HTTPFound("/")

    # Non-logged-in login
    return web.FileResponse('/DARLMID/html/login.html')


# Logout page
async def logout(request):
    # Not logged-in, redirect to /login
    if not (await is_logged_in(request)):
        raise web.HTTPFound("/login")

    # Logged-in, logout user
    web_response = web.HTTPFound("/login")

    # Delete the cookie
    web_response.del_cookie("DARLMID_key", domain = os.environ["MAIN_NODE_URL"])
    # Delete the local copy in Redis
    DARLMID_key = request.cookies["DARLMID_key"]
    await delete_cookie_key(DARLMID_key)

    # Return to login
    raise web_response


# Gets the sign-up data
async def action_sign_up(request):
    
    # Sign-up action GET is not allowed, redirect to sign up
    if request.method == "GET":
        raise web.HTTPFound('/sign_up')

    # If it fails, return a failure
    try:
        received_sign_up_data = await request.json()
    except:
        raise web.HTTPUnprocessableEntity()

    # Ensures that all JSON data inputs contain:
    # username, password, agreed to TOS
    necessary_fields = ["username", "password", "agreed to TOS"]
    if not check_keys_in_dict(received_sign_up_data, necessary_fields):
        return web.json_response({"Missing keys": ", ".join(missing_keys_in_dict(received_sign_up_data, necessary_fields))})

    username = sanitize_str_for_HTML(received_sign_up_data["username"])
    password = sanitize_str_for_HTML(received_sign_up_data["password"])
    agreed_to_TOS = received_sign_up_data["agreed to TOS"]

    if agreed_to_TOS != "yes":
        return web.json_response({"Output": "Failure", "Cause": "Must agree to Terms & Conditions"})


    # Verify if user already exists
    if username_in_db(username):
        return web.json_response({"Output": "Failure", "Cause": "User already exists"})

    # Adds user data to PostgreSQL
    create_new_user(username, password)

    # Return a JSON object with {username, cookie_ID}
    return web.json_response({"Output": "Success"})


# Logins a user
async def action_login(request):
    
    # Sign-up action GET is not allowed, redirect to sign up
    if request.method == "GET":
        raise web.HTTPFound('/login')

    # If it fails, return a failure
    try:
        received_sign_up_data = await request.json()
    except:
        raise web.HTTPUnprocessableEntity()

    # Ensures that all JSON data inputs contain:
    # username, password, agreed to TOS
    necessary_fields = ["username", "password"]
    if not check_keys_in_dict(received_sign_up_data, necessary_fields):
        return web.json_response({"Missing keys": ", ".join(missing_keys_in_dict(received_sign_up_data, necessary_fields))})

    username = sanitize_str_for_HTML(received_sign_up_data["username"])
    password = sanitize_str_for_HTML(received_sign_up_data["password"])

    # Verify username-password combinations
    if verify_username_password(username, password):

        # Generates a record in Redis
        obtained_key_ID = generate_key_identifier()

        cookie_max_age = 10000 # s

        # Generates a server record of the cookie in Redis, to verify it
        await generate_cookie_record(obtained_key_ID, username, cookie_max_age)

        web_response = web.json_response({"Output": "Success"})
        # Generates a cookie containing the username
        web_response.set_cookie("DARLMID_key", obtained_key_ID, domain = os.environ["MAIN_NODE_URL"], max_age = int(cookie_max_age))
        # Return a JSON object with {username, cookie_ID}
        return web_response
    else:
        return web.json_response({"Output": "Failure", "Cause": "Cannot login"})


# Obtain's all the user information for the session as stored in Redis
async def action_user_session_info(request):

    # Not logged-in, return empty
    if not (await is_logged_in(request)):
        web_response = web.json_response({})
        return web_response

    # Retrieves information
    obtained_session_info = await get_user_session_info(request.cookies["DARLMID_key"])
    web_response = web.json_response(obtained_session_info)
    return web_response


# Obtains vehicle and car information
async def retrieve_circuit_vehicle(request):

    # Not logged-in, redirect to /
    if not (await is_logged_in(request)):
        raise web.HTTPFound("/")

    # If it fails, return a failure
    try:
        received_cv_data = await request.json()
    except:
        raise web.HTTPUnprocessableEntity()

    # Ensures that all JSON data inputs contain: "circuit"
    necessary_fields = ["circuit"]
    if not check_keys_in_dict(received_cv_data, necessary_fields):
        return web.json_response({"Missing keys": ", ".join(missing_keys_in_dict(received_cv_data, necessary_fields))})

    chosen_circuit = received_cv_data["circuit"]

    circuit_file = "/DARLMID/circuits/" + chosen_circuit + ".json"

    # Checks if the circuit exists
    if not os.path.isfile(circuit_file):
        return web.json_response({"Output":"Failure", "Cause":"Circuit %s does not exist" % (chosen_circuit,)})

    with open(circuit_file, "r") as jf:
        necessary_info = json.load(jf)

    necessary_info["Output"] = "Success"

    return web.json_response(necessary_info)


# Receives the data
async def receive_demonstration_data(request):

    # Not logged-in, redirect to /
    if not (await is_logged_in(request)):
        raise web.HTTPFound("/")

    # If it fails, return a failure
    try:
        received_driving_data = await request.json()
    except:
        raise web.HTTPUnprocessableEntity()


    # Ensures necessary fields are there
    necessary_fields = ["actions taken", "intent"]
    if not check_keys_in_dict(received_driving_data, necessary_fields):
        return web.json_response({"Missing keys": ", ".join(missing_keys_in_dict(received_driving_data, necessary_fields))})

    positive_intent_location = "/DARLMID/data/positive/"
    negative_intent_location = "/DARLMID/data/negative/"

    if received_driving_data["intent"] == "positive":
        data_storage_location = positive_intent_location + uuid.uuid4().hex + ".json"
    else:
        data_storage_location = negative_intent_location + uuid.uuid4().hex + ".json"


    # Writes the data to location, datafile is named randomly
    with open(data_storage_location, "w") as jf:
        jf.write(json.dumps(received_driving_data, indent=4))

    return web.json_response({"Output":"Success"})



# Redirects to custom 404 page
async def handle_404_error(request):
    raise web.HTTPFound("/404.html")




def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except Exception:
            return await overrides[500](request)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404_error
    })
    app.middlewares.append(error_middleware)


DARLMID_web_app = web.Application()

# Main index
DARLMID_web_app.router.add_get("/", index)
DARLMID_web_app.router.add_get("/index", index)
DARLMID_web_app.router.add_get("/index.html", index)

# Sign-Up
DARLMID_web_app.router.add_get("/sign_up", sign_up)
DARLMID_web_app.router.add_get("/sign_up.html", sign_up)

# Login
DARLMID_web_app.router.add_get("/login", login)
DARLMID_web_app.router.add_get("/login.html", login)


# Sign-up action
DARLMID_web_app.router.add_get("/sign_up_action", action_sign_up)
DARLMID_web_app.router.add_post("/sign_up_action", action_sign_up)

# Login action
DARLMID_web_app.router.add_get("/login_action", action_login)
DARLMID_web_app.router.add_post("/login_action", action_login)

# Logout
DARLMID_web_app.router.add_get("/logout", logout)
DARLMID_web_app.router.add_get("/logout.html", logout)

# Obtaining user's information
DARLMID_web_app.router.add_get("/user_info", action_user_session_info)

# Driving, training an RL agent through demonstrations
DARLMID_web_app.router.add_get("/driving", driving)

# Retrieving circuit and vehicle information
DARLMID_web_app.router.add_post("/retrieve_circuit_vehicle", retrieve_circuit_vehicle)

# Receives demonstration data
DARLMID_web_app.router.add_post("/receive_demonstration_data", receive_demonstration_data)


# Error handling
setup_middlewares(DARLMID_web_app)

# To be run with gunicorn using
# -w (num cores + 1)
# main_node -> Docker container
# gunicorn traffic:DARLMID_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5
