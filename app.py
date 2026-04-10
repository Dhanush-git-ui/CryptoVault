# ===============================
# CryptoVault — Main App
# ===============================

from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User

# Import Blueprints
from routes.auth import auth_bp
from routes.crypto_routes import crypto_bp
from routes.dashboard import dashboard_bp

import os
app = Flask(__name__)
app.secret_key = 'supersafe_secret_key_for_sessions'

# DB Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aum_secure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login Manager Setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()


# Ensure secure storage directory exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'secure_vault')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ===============================
# REGISTER BLUEPRINTS
# ===============================
app.register_blueprint(auth_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(dashboard_bp)

# ===============================
# PAGE ROUTES (TEMPLATES)
# ===============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/simulation")
def simulation():
    return render_template("simulation.html")

@app.route("/research")
def research():
    return render_template("research.html")

# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)