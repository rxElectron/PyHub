
from flask import Blueprint

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug')
def debug_page():
    return "Welcome to the Debug page!"
