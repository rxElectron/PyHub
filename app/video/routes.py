
from flask import Blueprint

video_bp = Blueprint('video', __name__)

@video_bp.route('/video')
def video_page():
    return "Welcome to the Video page!"
