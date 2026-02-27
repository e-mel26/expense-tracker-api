import os
from datetime import timedelta


class Config:
    # =============================
    # OpenAPI / Swagger
    # =============================
    API_TITLE = "Expense Tracker API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # =============================
    # Database
    # =============================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =============================
    # JWT
    # =============================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-super-secret-key-change-me")

    # Token expiration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)