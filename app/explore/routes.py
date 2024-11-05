from . import explore
from flask import render_template

@explore.route('/')
def explore_page():
    return render_template('ai_ml_tools.html')
