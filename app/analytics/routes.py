from . import analytics
from flask import render_template

@analytics.route('/')
def index():
    return render_template('analytics/index.html')
