
from flask import Blueprint

project_manager_bp = Blueprint('project_manager', __name__)

@project_manager_bp.route('/project_manager')
def project_manager_page():
    return "Welcome to the Project Manager page!"
