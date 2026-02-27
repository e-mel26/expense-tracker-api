from flask import Flask
from dotenv import load_dotenv
import os

from .extensions import db, jwt, migrate, api


def create_app():
    # Load environment variables from .env
    load_dotenv(override=True)

    app = Flask(__name__)

    # Import config AFTER loading env
    from .config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import blueprints
    from app.routes.auth import blp as auth_blp
    from app.routes.categories import blp as categories_blp
    from app.routes.expenses import blp as expenses_blp

    # Register blueprints
    api.register_blueprint(auth_blp)
    api.register_blueprint(categories_blp)
    api.register_blueprint(expenses_blp)

    return app