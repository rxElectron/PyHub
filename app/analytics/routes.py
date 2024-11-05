from . import analytics
from flask import render_template

@analytics.route('/analytics')
def analytics_page():
    return render_template('analytics.html')
