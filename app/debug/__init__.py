from flask import Blueprint

debug = Blueprint('debug', __name__)

from . import routes
