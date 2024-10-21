
from flask import Blueprint

comparator_bp = Blueprint('comparator', __name__)

@comparator_bp.route('/comparator')
def comparator_page():
    return "Welcome to the Code Comparator page!"
