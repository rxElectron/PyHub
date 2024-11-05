from flask import Blueprint

code_comparator = Blueprint('code_comparator', __name__)

from . import routes
