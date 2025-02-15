# exception_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse

from config.logging import logger


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )
