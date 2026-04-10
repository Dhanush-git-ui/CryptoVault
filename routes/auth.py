# ===============================
# auth.py
# ===============================

from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from routes.dashboard import log_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    # If the user sends raw text format user:pass
    if request.is_json:
        data = request.get_json()
        if isinstance(data, str) and ":" in data:
            username, password = data.split(":", 1)
        else:
            username = data.get("username")
            password = data.get("password")
    else:
         return jsonify({"message": "Invalid format"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = None
    password = None

    if isinstance(data, str) and ":" in data:
        username, password = data.split(":", 1)
    elif isinstance(data, dict):
        username = data.get("username")
        password = data.get("password")

    if not username or not password:
        log_login(success=False)
        return jsonify({"message": "Invalid format"}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        log_login(success=True)
        return jsonify({
            "session_token": "authenticated_via_cookie"
        })
    else:
        log_login(success=False)
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@auth_bp.route("/users", methods=["GET"])
@login_required
def get_users():
    users = User.query.all()
    # Don't include current user in the 'share with' list
    return jsonify([{"id": u.id, "username": u.username} for u in users if u.id != current_user.id])