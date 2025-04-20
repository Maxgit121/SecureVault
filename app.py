import os
import sqlite3
from flask import Flask
from flask_login import LoginManager

# Initialize Flask application
app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure SQLite database (password.db)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///password.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models here after initializing app to avoid circular imports
from models import db, User

# Create database tables
with app.app_context():
    db.init_app(app)
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
