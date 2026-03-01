from flask import Flask
import os

from .extensions import db, jwt, migrate, api


def create_app():
    # Only load .env locally (Render provides env vars in dashboard)
    if os.getenv("RENDER") is None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

    app = Flask(__name__)

    # Load config (reads DATABASE_URL, JWT_SECRET_KEY, etc.)
    from .config import Config
    app.config.from_object(Config)

    # Init extensions
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