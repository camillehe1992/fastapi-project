# lifespan.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.logging import logger
from db.utils import create_tables


@asynccontextmanager
async def lifespan(app):
    # Startup logic
    logger.info("Application startup: Initializing resources...")
    # Add your startup logic here (e.g., connect to a database, load models, etc.)

    yield  # The application runs here

    # Shutdown logic
    logger.info("Application shutdown: Cleaning up resources...")
    # Add your shutdown logic here (e.g., close database connections, etc.)


# Lifespan function to initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    create_tables()
    yield  # The application runs here
    logger.info("Shutting down...")
