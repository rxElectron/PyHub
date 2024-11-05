from . import explore
from flask import render_template

@explore.route('/explore')
def explore_page():
    return render_template('explore.html')
