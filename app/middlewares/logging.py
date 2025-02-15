# logging_middleware.py
from fastapi import Request

from config.logging import logger


# Middleware to log requests and responses
async def log_requests_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Outgoing response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        raise
