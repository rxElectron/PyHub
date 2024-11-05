from flask import Blueprint

support_help = Blueprint('support_help', __name__)

from . import routes
