import aiohttp
from aiohttp import web
from routes import setup_routes
from middleware import logger_middleware

app = web.Application()
setup_routes(app)

# Add the logger middleware
app.middlewares.append(logger_middleware)

web.run_app(app)
# 