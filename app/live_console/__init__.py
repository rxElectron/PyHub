from flask import Blueprint

live_console = Blueprint('live_console', __name__)

from . import routes
