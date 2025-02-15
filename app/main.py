from fastapi import FastAPI

from config.settings import settings
from config.openapi import custom_openapi
from middlewares.logging import log_requests_middleware
from routers.api import router
from exception_handlers import global_exception_handler
from lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
    debug=bool(settings.DEBUG),
)

# Add the middleware to the app
app.middleware("http")(log_requests_middleware)

if settings.DEBUG:
    origins = ["*"]
else:
    origins = [str(origin).strip(",") for origin in settings.ORIGINS]

# Assign the custom OpenAPI schema to the app
# Use lambda to make sure the swagger ui is rendered dynamically
app.openapi = lambda: custom_openapi(app)

# Include routers
app.include_router(router)

# Add the exception handler to the app
app.add_exception_handler(Exception, global_exception_handler)
