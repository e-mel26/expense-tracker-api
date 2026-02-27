# app/routes/__init__.py
from .auth import blp as auth_blp
from .categories import blp as categories_blp
from .expenses import blp as expenses_blp

__all__ = ["auth_blp", "categories_blp", "expenses_blp"]