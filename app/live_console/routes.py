
from flask import Blueprint

live_console = Blueprint('live_console', __name__)

@live_console.route('/live_console')
def live_console_page():
    return "Welcome to the Live Console page!"
