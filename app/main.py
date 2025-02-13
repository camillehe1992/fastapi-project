from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.settings import settings
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
    title=settings.TITLE,
)


if settings.DEBUG:
    origins = ["*"]
else:
    origins = [str(origin).strip(",") for origin in settings.ORIGINS]


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


app.include_router(router)
