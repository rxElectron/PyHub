from . import profile
from flask import render_template

@profile.route('/profile')
def profile_page():
    return render_template('profile.html')
