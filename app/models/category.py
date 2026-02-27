from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)  # ✅ auto id
    name = db.Column(db.String(80), nullable=False, unique=True)

    # optional: if you have user-specific categories later
    user_id = db.Column(db.Integer, nullable=True)