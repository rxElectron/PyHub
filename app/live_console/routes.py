
from flask import Blueprint

live_console_bp = Blueprint('live_console', __name__)

@live_console_bp.route('/live_console')
def live_console_page():
    return "Welcome to the Live Console page!"
