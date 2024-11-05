from . import code_comparator
from flask import render_template

@code_comparator.route('/code_comparator')
def comparator_page():
    return render_template('ai_ml_tools.html')
