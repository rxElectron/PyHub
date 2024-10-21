
from flask import Blueprint

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/learning')
def learning_page():
    return "Welcome to the Learning page!"
