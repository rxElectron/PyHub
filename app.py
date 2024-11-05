import socket
import threading
import platform
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, redirect, url_for, jsonify
import logging
import os
from pathlib import Path
import sys
import signal
import shutil
import requests
from flask import request, jsonify

# ----------------------------
# Configuration and Constants
# ----------------------------

# Define constants
DEFAULT_HOST = "1.1.1.1"
DEFAULT_PORT = 53
DEFAULT_TIMEOUT = 3
FLASK_PORT = 5000
ELECTRON_APP_DIR = 'electron_app'
CONFIG_MODULE = 'config.Config'

# ----------------------------
# Logging Configuration
# ----------------------------

def setup_logging():
    """
    Configures logging to output to both console and a file.
    """
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    log_file = Path(__file__).parent / "app.log"

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # Root logger
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# Initialize logging
setup_logging()
logging.info("Application starting...")

# ----------------------------
# Flask App Initialization
# ----------------------------

from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for requests from your local server and the 0xelectron.ir domain
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000", "https://0xelectron.ir"]}})

# Load configurations from config.py
try:
    app.config.from_object(CONFIG_MODULE)
    logging.info(f"Loaded configuration from {CONFIG_MODULE}.")
except Exception as e:
    logging.error(f"Failed to load configuration from {CONFIG_MODULE}: {e}")
    sys.exit(1)

# Register blueprints
try:
    from app.debug.routes import debug
    from app.explore.routes import explore
    from app.ai_ml_tools.routes import ai_ml_tools
    from app.analytics.routes import analytics
    from app.code_comparator.routes import code_comparator
    from app.learning.routes import learning
    from app.live_console.routes import live_console
    from app.profile.routes import profile
    from app.project_manager.routes import project_manager
    from app.settings.routes import settings
    from app.support_help.routes import support_help

    app.register_blueprint(debug)
    app.register_blueprint(explore)
    app.register_blueprint(ai_ml_tools)
    app.register_blueprint(analytics)
    app.register_blueprint(code_comparator)
    app.register_blueprint(learning)
    app.register_blueprint(live_console)
    app.register_blueprint(profile)
    app.register_blueprint(project_manager)
    app.register_blueprint(settings)
    app.register_blueprint(support_help)
    logging.info("Registered all blueprints successfully.")
except ImportError as e:
    logging.error(f"Failed to import blueprints: {e}")
    sys.exit(1)

# ----------------------------
# Utility Functions
# ----------------------------

def is_connected(host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT):
    """
    Check internet connectivity by attempting to connect to a specified host and port.
    """
    try:
        socket.create_connection((host, port), timeout=timeout)
        logging.debug("Internet connection check: ONLINE.")
        return True
    except OSError:
        logging.debug("Internet connection check: OFFLINE.")
        return False

def open_electron():
    """
    Launch the Electron application.
    """
    try:
        current_dir = Path(__file__).parent
        electron_dir = current_dir / ELECTRON_APP_DIR

        if not electron_dir.exists():
            msg = f"Electron app directory not found: {electron_dir}"
            logging.error(msg)
            messagebox.showerror("Error", msg)
            return

        # Check if yarn is installed
        if not shutil.which("yarn"):
            msg = "Yarn is not installed or not found in PATH."
            logging.error(msg)
            messagebox.showerror("Error", msg)
            return

        logging.info(f"Launching Electron app from {electron_dir}...")
        subprocess.Popen(['yarn', 'start'], cwd=electron_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Electron app launched successfully.")
    except Exception as e:
        logging.error(f"Failed to launch Electron app: {e}")
        messagebox.showerror("Error", f"Failed to launch Electron app: {e}")

def prompt_user():
    """
    Prompt the user to choose between Electron App Mode or Browser Mode.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        answer = messagebox.askquestion(
            "Select Mode",
            "Do you want to use the App Mode (Electron)?\n\nClick 'Yes' for Electron or 'No' for Browser."
        )

        if answer == 'yes':
            open_electron()
        else:
            url = f"http://127.0.0.1:{FLASK_PORT}/"
            logging.info(f"Opening browser to {url}...")
            webbrowser.open(url)
    except Exception as e:
        logging.error(f"Error during user prompt: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        root.destroy()

def start_flask():
    """
    Start the Flask server.
    """
    try:
        # Suppress Flask's default logging to avoid duplication
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        logging.info(f"Starting Flask server on port {FLASK_PORT}...")
        app.run(debug=False, port=FLASK_PORT, use_reloader=False)
    except Exception as e:
        logging.error(f"Failed to start Flask server: {e}")

def shutdown_application(signum, frame):
    """
    Handle graceful shutdown on receiving termination signals.
    """
    logging.info("Shutting down application...")
    sys.exit(0)

# ----------------------------
# Flask Routes
# ----------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proxy_to_https')
def proxy_to_https():
    user_ip = request.remote_addr
    headers = {'X-Forwarded-For': user_ip}
    response = requests.get("https://targetsite.com/api", headers=headers)
    return jsonify(response.json())

@app.route('/online')
def online_features():
    if is_connected():
        response = {
            "status": "online",
            "message": "You are online! Access AI, search, and video streaming."
        }
        logging.info("User accessed online features.")
        return jsonify(response)
    else:
        logging.info("User attempted to access online features while offline.")
        return redirect(url_for('offline'))

@app.route('/offline')
def offline():
    response = {
        "status": "offline",
        "message": "You are offline! Access local content and offline features."
    }
    logging.info("User accessed offline features.")
    return jsonify(response)

# ----------------------------
# Main Execution
# ----------------------------

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, shutdown_application)
    signal.signal(signal.SIGTERM, shutdown_application)

    # Start Flask server in a separate daemon thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Wait briefly to ensure Flask server starts before opening browser
    threading.Event().wait(1)

    # Prompt user to select mode
    prompt_user()

    # Keep the main thread alive while Flask server is running
    try:
        while flask_thread.is_alive():
            flask_thread.join(timeout=1)
    except KeyboardInterrupt:
        shutdown_application(None, None)

if __name__ == "__main__":
    main()
