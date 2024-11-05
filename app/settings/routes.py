
from flask import Blueprint

settings = Blueprint('settings', __name__)

@settings.route('/settings')
def settings_page():
    return "Welcome to the Settings page!"
