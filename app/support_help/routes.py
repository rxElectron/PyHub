from . import support_help
from flask import render_template

@support_help.route('/support_help')
def support_help_page():
    return render_template('support_help.html')
