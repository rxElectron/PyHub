
from flask import Blueprint

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
def settings_page():
    return "Welcome to the Settings page!"
