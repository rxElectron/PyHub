from . import support_help
from flask import render_template

@support_help.route('/')
def index():
    return render_template('support_help/index.html')
