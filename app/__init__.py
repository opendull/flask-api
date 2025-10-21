from flask import Flask
from flask_jwt_extended import JWTManager
from app.utils.database import db
from app.config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app
