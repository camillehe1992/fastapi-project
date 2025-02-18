from fastapi.middleware.cors import CORSMiddleware

from settings import settings


def add_cors_middleware(app):
    """
    Add CORS middleware to the FastAPI app.

    :param app: The FastAPI app instance.
    """
    if settings.DEBUG:
        allow_origins = ["*"]
    else:
        allow_origins = [str(origin).strip(",") for origin in settings.ORIGINS]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
