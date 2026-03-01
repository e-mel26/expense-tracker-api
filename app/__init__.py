import os
from flask import Flask

# Optional: only used locally
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from .extensions import db, jwt, migrate, api


def create_app():
    # Load .env ONLY when running locally (not on Render)
    if load_dotenv and os.getenv("RENDER") is None:
        load_dotenv()

    app = Flask(__name__)

    # Load config (expects env vars on Render)
    from .config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Register blueprints
    from app.routes.auth import blp as auth_blp
    from app.routes.categories import blp as categories_blp
    from app.routes.expenses import blp as expenses_blp

    api.register_blueprint(auth_blp)
    api.register_blueprint(categories_blp)
    api.register_blueprint(expenses_blp)

    return app