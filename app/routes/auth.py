from flask import Blueprint, request, jsonify
from app.utils.database import db
from app.models.user import User
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = User(email=email, password_hash=hashed_pw, name=name)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        "message": "User registered successfully",
        "token": access_token,
        "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name
        }
    }), 201


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }), 200
