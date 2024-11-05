from flask import Blueprint

ai_ml_tools = Blueprint('ai_ml_tools', __name__)

from . import routes
