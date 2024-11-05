from . import ai_ml_tools
from flask import render_template

@ai_ml_tools.route('/')
def index():
    return render_template('ai_ml_tools/index.html')
