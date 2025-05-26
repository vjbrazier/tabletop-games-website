"""
The login page, as well as functions related to logging in/out.
"""
# Third-party imports
from flask_login import LoginManager

# Custom imports
from core import app
from user_manager import UserManager

user_manager = UserManager()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    """
    Loads the Users with Flask's user_loader.
    """
    return user_manager.users.get(username)

