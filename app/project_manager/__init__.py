from flask import Blueprint

project_manager = Blueprint('project_manager', __name__)

from . import routes
