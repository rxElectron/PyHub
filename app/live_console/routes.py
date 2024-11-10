from . import live_console
from flask import render_template

@live_console.route('/live_console')
def live_console_page():
    return render_template('live_console.html')
