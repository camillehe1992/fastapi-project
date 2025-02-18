# lifespan.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from logger import logger
from db.utils import create_tables


# Lifespan function to initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    create_tables()
    yield  # The application runs here
    logger.info("Shutting down...")
