from contextlib import asynccontextmanager
from fastapi import FastAPI

from config.settings import settings
from routers.api import router
from db.utils import create_tables
from config.openapi import custom_openapi


# Lifespan function to initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    create_tables()
    yield  # The application runs here
    print("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
    debug=bool(settings.DEBUG),
)


if settings.DEBUG:
    origins = ["*"]
else:
    origins = [str(origin).strip(",") for origin in settings.ORIGINS]

# Assign the custom OpenAPI schema to the app
app.openapi = lambda: custom_openapi(app)

# Include routers
app.include_router(router)
