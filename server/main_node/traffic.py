"""
BASICS

Directs TCP traffic and executes the appropriate commands or returning the correct file
"""

import uuid

from aiohttp import web

from helper import *
from helper_postgres import *



# Serves Index (main HTML file)
async def index(request):
    # Non-logged-in index
    return web.FileResponse('/expert_seas/html/index.html')



# Sign-Up page
async def sign_up(request):
    # Non-logged-in sign-up
    return web.FileResponse('/expert_seas/html/sign_up.html')


# Login page
async def login(request):
    # Non-logged-in login
    return web.FileResponse('/expert_seas/html/login.html')



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

    username = received_sign_up_data["username"]
    password = received_sign_up_data["password"]
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


expert_seas_web_app = web.Application()

# Main index
expert_seas_web_app.router.add_get("/", index)
expert_seas_web_app.router.add_get("/index", index)
expert_seas_web_app.router.add_get("/index.html", index)

# Sign-Up
expert_seas_web_app.router.add_get("/sign_up", sign_up)
expert_seas_web_app.router.add_get("/sign_up.html", sign_up)

# Login
expert_seas_web_app.router.add_get("/login", login)
expert_seas_web_app.router.add_get("/login.html", login)


# Sign-up action
expert_seas_web_app.router.add_get("/sign_up_action", action_sign_up)
expert_seas_web_app.router.add_post("/sign_up_action", action_sign_up)



# Error handling
setup_middlewares(expert_seas_web_app)

# To be run with gunicorn using
# -w (num cores + 1)
# main_node -> Docker container
# gunicorn traffic:expert_seas_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5
