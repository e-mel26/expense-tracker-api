from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Category
from app.schemas import CategorySchema


blp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories",
    description="Category operations",
)


# -------------------------
# GET all categories
# -------------------------
@blp.get("/")
@blp.response(200, CategorySchema(many=True))
def get_categories():
    """Get all categories"""
    categories = Category.query.order_by(Category.id.asc()).all()
    return categories


# -------------------------
# CREATE category
# -------------------------
@blp.post("/")
@blp.arguments(CategorySchema)
@blp.response(201, CategorySchema)
def create_category(data):
    """Create a new category"""

    # Prevent duplicates
    existing = Category.query.filter_by(name=data["name"]).first()
    if existing:
        return {"message": "Category already exists"}, 409

    category = Category(name=data["name"])

    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"message": "Database error"}, 400

    return category


# -------------------------
# Seed default categories
# -------------------------
@blp.post("/seed")
def seed_categories():
    """Seed default categories"""

    default_names = [
        "Food",
        "Transport",
        "Bills",
        "Shopping",
        "Health",
        "Entertainment",
    ]

    created = 0

    for name in default_names:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            created += 1

    db.session.commit()

    return {
        "message": f"Seeded categories. Added {created} new categories."
    }, 201