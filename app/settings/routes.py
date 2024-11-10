from . import settings
from flask import render_template

@settings.route('/settings')
def settings_page():
    return render_template('settings.html')
