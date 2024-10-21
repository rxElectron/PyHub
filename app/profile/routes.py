
from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile_page():
    return "Welcome to the Profile page!"
