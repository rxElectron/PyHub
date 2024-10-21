
from flask import Blueprint

explore_bp = Blueprint('explore', __name__)

@explore_bp.route('/explore')
def explore_page():
    return "Welcome to the Explore page!"
