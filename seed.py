from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Only add if they don't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=generate_password_hash('password123'))
        db.session.add(admin)
    if not User.query.filter_by(username='alice').first():
        alice = User(username='alice', password_hash=generate_password_hash('password123'))
        db.session.add(alice)
    if not User.query.filter_by(username='bob').first():
        bob = User(username='bob', password_hash=generate_password_hash('password123'))
        db.session.add(bob)
    
    db.session.commit()
    print("✅ Created users: admin, alice, bob (Password for all: password123)")
