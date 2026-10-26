from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask import Flask
import os

# Setup Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flask-Login & Bcrypt setup
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Mock user database
user_db = {
    "admin": bcrypt.generate_password_hash("password123").decode('utf-8')
}

# User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in user_db:
        return User(user_id)
    return None

# Login validation
def validate_login(username, password):
    if username in user_db and bcrypt.check_password_hash(user_db[username], password):
        return True
    return False
