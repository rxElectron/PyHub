from . import project_manager
from flask import render_template

@project_manager.route('/project_manager')
def project_manager_page():
    return render_template('project_manager.html')
