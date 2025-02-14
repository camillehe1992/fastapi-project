from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from config.settings import settings
from routers.api import router
from db.utils import create_tables


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


# Custom OpenAPI schema to include securitySchemes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.TITLE,
        version=settings.VERSION,
        description="API with OAuth2 security",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Optional: Specify the token format
        }
    }

    # Apply the security scheme globally
    # openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Include routers
app.include_router(router)
