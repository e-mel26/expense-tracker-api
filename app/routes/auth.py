from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User
from app.schemas.auth import RegisterSchema, LoginSchema, UserOutSchema

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="Authentication")


@blp.post("/register")
@blp.arguments(RegisterSchema)
@blp.response(201, UserOutSchema)
def register(data):
    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        abort(409, message="Email already registered")

    user = User(
        name=data["name"].strip(),
        email=email,
        password_hash=generate_password_hash(data["password"]),
    )

    db.session.add(user)
    db.session.commit()
    return user


@blp.post("/login")
@blp.arguments(LoginSchema)
def login(data):
    email = data["email"].lower().strip()
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        abort(401, message="Invalid email or password")

    token = create_access_token(identity=str(user.id))
    return {"access_token": token}


@blp.get("/me")
@jwt_required()
@blp.response(200, UserOutSchema)
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return user