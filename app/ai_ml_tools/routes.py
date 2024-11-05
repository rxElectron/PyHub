from . import ai_ml_tools
from flask import render_template

@ai_ml_tools.route('/ai_ml_tools')
def show_ai_ml_tools():
    return render_template('ai_ml_tools.html')

# def ai_ml_tools():
#     return render_template('ai_ml_tools.html')
