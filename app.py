# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# PyHub/app.py
# ----------------------------------------------------------------

import socket
import requests
import platform
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
from flask_socketio import SocketIO
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_cors import CORS
import logging
from pathlib import Path
import sys
import signal
import shutil
import shlex
import threading
import base64  # Added base64 module

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
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
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
app = Flask(__name__)

# Allow CORS for requests from your local server and the 0xelectron.ir domain
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000", "https://0xelectron.ir"]}})

# Initialize SocketIO with appropriate CORS settings
socketio = SocketIO(app, cors_allowed_origins=["http://127.0.0.1:5000", "https://0xelectron.ir"])

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

def is_yarn_installed():
    """
    Check if Yarn is installed and accessible.
    """
    return shutil.which("yarn") is not None or shutil.which("yarn.cmd") is not None

def get_yarn_command():
    """
    Return the appropriate yarn command based on the operating system.
    """
    if platform.system() == "Windows":
        return ["yarn.cmd", "start"]
    else:
        return ["yarn", "start"]

def is_electron_app_ready(electron_dir):
    """
    Ensure that the Electron app directory contains necessary files.
    """
    required_files = ['package.json', 'yarn.lock']
    for file in required_files:
        if not (electron_dir / file).exists():
            logging.error(f"Required file '{file}' not found in {electron_dir}.")
            return False
    return True

def open_electron():
    """
    Launch the Electron application.
    """
    try:
        current_dir = Path(__file__).parent.resolve()
        electron_dir = current_dir / ELECTRON_APP_DIR
        logging.debug(f"Current directory: {current_dir}")
        logging.debug(f"Electron app directory: {electron_dir}")

        if not electron_dir.exists():
            msg = f"Electron app directory not found: {electron_dir}"
            logging.error(msg)
            messagebox.showerror("Error", msg)
            return

        if not is_electron_app_ready(electron_dir):
            msg = (
                f"The Electron app directory is missing required files.\n"
                f"Please ensure that {', '.join(['package.json', 'yarn.lock'])} exist in {electron_dir}."
            )
            logging.error(msg)
            messagebox.showerror("Error", msg)
            return

        if not is_yarn_installed():
            msg = (
                "Yarn is not installed or not found in PATH.\n"
                "Please install Yarn from https://classic.yarnpkg.com/en/docs/install#windows-stable and ensure it's added to your PATH."
                "\n\nWould you like to visit the Yarn installation page now?"
            )
            logging.error("Yarn not found.")
            answer = messagebox.askyesno("Yarn Not Found", msg)
            if answer:
                webbrowser.open("https://classic.yarnpkg.com/en/docs/install#windows-stable")
            return

        logging.info(f"Launching Electron app from {electron_dir}...")
        yarn_command = get_yarn_command()
        logging.debug(f"Yarn command: {yarn_command}")

        process = subprocess.Popen(
            yarn_command,
            cwd=electron_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False  # Recommended to set shell=False for security
        )

        # Optionally, read stdout and stderr in real-time
        def log_subprocess_output(proc):
            try:
                for line in proc.stdout:
                    logging.info(f"Electron: {line.strip()}")
                for line in proc.stderr:
                    logging.error(f"Electron Error: {line.strip()}")
            except Exception as e:
                logging.error(f"Error reading Electron process output: {e}")

        threading.Thread(target=log_subprocess_output, args=(process,), daemon=True).start()

        # Wait for the Electron process to complete
        process.wait()

        if process.returncode != 0:
            msg = f"Electron app failed to start. Please check the logs for more details."
            logging.error(msg)
            messagebox.showerror("Error", msg)
        else:
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
            url = f"http://127.0.0.1:{FLASK_PORT}/live_console"
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
        socketio.run(app, debug=False, port=FLASK_PORT, use_reloader=False)
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
    try:
        response = requests.get("https://targetsite.com/api", headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logging.error(f"Proxy request failed: {e}")
        return jsonify({"error": "Failed to fetch data from target site."}), 500

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
# Register Socket.IO Namespaces
# ----------------------------

def setup_socketio_namespaces(socketio):
    """
    Registers all Socket.IO namespaces.
    """
    from app.live_console.routes import PythonConsoleNamespace, TerminalNamespace
    socketio.on_namespace(PythonConsoleNamespace('/python_console'))
    socketio.on_namespace(TerminalNamespace('/terminal'))

# ----------------------------
# Main Execution
# ----------------------------

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, shutdown_application)
    signal.signal(signal.SIGTERM, shutdown_application)

    # Register Socket.IO namespaces
    setup_socketio_namespaces(socketio)

    # Start Flask server in a separate daemon thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Wait briefly to ensure Flask server starts before opening browser or Electron
    threading.Event().wait(1)

    # Prompt user to select mode
    threading.Thread(target=prompt_user, daemon=True).start()

    # Keep the main thread alive while Flask server is running
    try:
        while flask_thread.is_alive():
            flask_thread.join(timeout=1)
    except KeyboardInterrupt:
        shutdown_application(None, None)

if __name__ == "__main__":
    main()
