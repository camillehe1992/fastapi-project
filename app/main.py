from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.settings import settings
from utils.init_db import create_tables
from api.v1.routers import items, users, todos


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
    title=settings.TITLE,
)


if settings.DEBUG:
    origins = ["*"]
else:
    origins = [str(origin).strip(",") for origin in settings.ORIGINS]


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# Register Routers
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(todos.router, prefix="/api/v1/todos", tags=["todos"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
