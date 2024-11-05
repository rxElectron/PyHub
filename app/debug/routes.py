from . import debug
from flask import render_template

@debug.route('/')
def index():
    return render_template('ai_ml_tools.html')
