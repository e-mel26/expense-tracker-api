from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api

db = SQLAlchemy(
    engine_options={
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
)

migrate = Migrate()
jwt = JWTManager()
api = Api()