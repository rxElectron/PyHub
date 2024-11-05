from . import learning
from flask import render_template

@learning.route('/learning')
def learning_page():
    return render_template('ai_ml_tools.html')




