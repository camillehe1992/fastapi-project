from fastapi.openapi.utils import get_openapi

from config.settings import settings


# Custom OpenAPI schema to include securitySchemes
def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.TITLE,
        version=settings.VERSION,
        description="A Swagger for FastAPI Application",
        routes=app.routes,
    )

    # Customize the securitySchemes
    components = openapi_schema.get("components", {})

    components["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Optional: Specify the token format
        }
    }

    # Apply the security scheme globally
    # openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    # Save the custom schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema
