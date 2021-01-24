"""
BASICS

Directs TCP traffic and executes the appropriate commands or returning the correct file
"""

from aiohttp import web

async def index(request):
    return web.Response(text="Welcome home!")


expert_seas_web_app = web.Application()
expert_seas_web_app.router.add_get('/', index)

# To be run with gunicorn using
# -w (num cores + 1)
# main_node -> Docker container
# gunicorn traffic:expert_seas_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5
