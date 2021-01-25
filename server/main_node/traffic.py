"""
BASICS

Directs TCP traffic and executes the appropriate commands or returning the correct file
"""

from aiohttp import web


# Serves Index (main HTML file)
async def index(request):
    # Non-logged-in index
    return web.FileResponse('/expert_seas/html/index.html')


# Redirects to custom 404 page
async def handle_404_error(request):
    raise web.HTTPFound('/404.html')




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
expert_seas_web_app.router.add_get('/', index)
expert_seas_web_app.router.add_get('/index', index)
expert_seas_web_app.router.add_get('/index.html', index)


# Error handling
setup_middlewares(expert_seas_web_app)

# To be run with gunicorn using
# -w (num cores + 1)
# main_node -> Docker container
# gunicorn traffic:expert_seas_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5
