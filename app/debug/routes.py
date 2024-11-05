from . import debug
from flask import render_template

@debug.route('/debug')
def debug_page():
    return render_template('debug.html')
