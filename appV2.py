# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# Copyright 2024    PyHub/appV2.py 

import socket
import threading
import platform
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_socketio import SocketIO, emit
import logging
import os
import time
import urllib.request
from pathlib import Path
import sys
import shutil

# ----------------------------
# Configuration and Constants
# ----------------------------

# Define constants
DEFAULT_HOST = "8.8.8.8"
DEFAULT_PORT = 53
DEFAULT_TIMEOUT = 3
FLASK_PORT = 5000
ELECTRON_APP_DIR = 'electron_app'
CONFIG_MODULE = 'config.Config'
HEALTH_ENDPOINT = '/health'
HOME_URL = f'http://127.0.0.1:{FLASK_PORT}/'

# ----------------------------
# Logging Configuration
# ----------------------------

def setup_logging():
    """
    Configures logging to output to both console and a file with timestamped format.
    """
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = Path(__file__).parent / "app.log"

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)  # Set to INFO to reduce console verbosity

    # Root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

# Initialize logging
setup_logging()
logging.info("Application starting...")

# ----------------------------
# Flask App Initialization
# ----------------------------

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# Load configurations from config.py
try:
    app.config.from_object(CONFIG_MODULE)
    logging.info("Configurations loaded from config.py")
except Exception as e:
    logging.error(f"Failed to load configurations: {e}")
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
    logging.info("All blueprints registered successfully.")
except ImportError as e:
    logging.error(f"Failed to register blueprints: {e}")
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
        logging.info("Internet connection is available.")
        return True
    except OSError as e:
        logging.warning(f"No internet connection: {e}")
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
    missing_files = [file for file in required_files if not (electron_dir / file).exists()]
    if missing_files:
        logging.error(f"Missing required files in Electron app directory: {', '.join(missing_files)}")
        return False
    logging.info("Electron app directory contains all required files.")
    return True

def get_installed_browsers():
    """
    Detect installed browsers based on the operating system.
    Returns a list of tuples: (browser_name, browser_path)
    """
    browsers = []
    try:
        if platform.system() == "Windows":
            paths = {
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            }
        elif platform.system() == "Darwin":
            paths = {
                "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
                "safari": "/Applications/Safari.app/Contents/MacOS/Safari",
                "brave": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            }
        elif platform.system() == "Linux":
            paths = {
                "google-chrome": "google-chrome",
                "firefox": "firefox",
                "chromium-browser": "chromium-browser",
                "brave-browser": "brave-browser"
            }
        else:
            logging.warning(f"Unsupported operating system: {platform.system()}")
            return browsers

        for browser, path in paths.items():
            try:
                if platform.system() == "Linux":
                    # For Linux, check if the browser is in PATH
                    if shutil.which(browser):
                        browsers.append((browser, browser))  # browser name and command
                        logging.info(f"{browser} detected in PATH.")
                else:
                    # For Windows and macOS, check if the executable exists
                    if Path(path).exists():
                        browsers.append((browser, path))  # browser name and path
                        logging.info(f"{browser.capitalize()} detected at {path}.")
            except Exception as e:
                logging.error(f"Failed to check browser {browser}: {e}")
    except Exception as e:
        logging.error(f"Failed to detect installed browsers: {e}")
    return browsers

def open_browser(browser_name, browser_path, url):
    """
    Open a specific browser with the provided URL.
    """
    try:
        logging.info(f"Attempting to open {browser_name} with URL: {url}")
        if platform.system() == "Windows":
            subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Linux":
            subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"{browser_name.capitalize()} browser opened successfully with URL: {url}")
    except Exception as e:
        logging.error(f"Failed to open {browser_name}: {e}")
        messagebox.showerror("Browser Error", f"Failed to open {browser_name}: {e}")
        # Prompt to use Electron
        if messagebox.askyesno("Open Electron", f"Do you want to open the application in Electron instead of {browser_name}?"):
            open_electron()
        else:
            logging.info("User chose not to open Electron.")

def open_default_browser(url):
    """
    Open the default system browser with the provided URL.
    """
    try:
        logging.info(f"Attempting to open default browser with URL: {url}")
        webbrowser.open(url)
        logging.info(f"Default browser opened successfully with URL: {url}")
    except Exception as e:
        logging.error(f"Failed to open default browser: {e}")
        messagebox.showerror("Browser Error", f"Failed to open default browser: {e}")
        # Prompt to use Electron
        if messagebox.askyesno("Open Electron", "Do you want to open the application in Electron instead of the default browser?"):
            open_electron()
        else:
            logging.info("User chose not to open Electron.")

def open_electron():
    """
    Launch the Electron application using Yarn.
    """
    try:
        logging.info("Attempting to start Electron app.")

        # Determine the absolute path to the Electron app directory
        current_dir = Path(__file__).parent.resolve()
        electron_dir = current_dir / ELECTRON_APP_DIR

        if not electron_dir.exists():
            msg = f"Electron app directory not found: {electron_dir}"
            logging.error(msg)
            messagebox.showerror("Error", msg)
            return

        if not is_electron_app_ready(electron_dir):
            msg = (
                f"The Electron app directory is missing required files.\n"
                f"Please ensure that package.json and yarn.lock exist in {electron_dir}."
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

        yarn_command = get_yarn_command()
        logging.debug(f"Yarn command: {yarn_command}")

        # Launch Electron app using subprocess.Popen
        process = subprocess.Popen(
            yarn_command,
            cwd=str(electron_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False  # Recommended to set shell=False for security
        )

        # Function to log subprocess output
        def log_subprocess_output(pipe, log_type):
            for line in iter(pipe.readline, ''):
                if line:
                    logging.info(f"Electron {log_type}: {line.strip()}")
            pipe.close()

        # Start threads to read stdout and stderr
        threading.Thread(target=log_subprocess_output, args=(process.stdout, "STDOUT"), daemon=True).start()
        threading.Thread(target=log_subprocess_output, args=(process.stderr, "STDERR"), daemon=True).start()

        logging.info("Electron app started successfully.")
    except FileNotFoundError:
        logging.error("Yarn is not installed or not found in PATH.")
        messagebox.showerror("Error", "Yarn is not installed or not found in PATH.")
    except Exception as e:
        logging.error(f"Failed to start Electron: {e}")
        messagebox.showerror("Error", f"Failed to start Electron: {e}")

def prompt_user():
    """
    Prompt the user with a GUI to choose between available browsers or Electron.
    """
    try:
        # Tkinter must run in the main thread
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        browsers = get_installed_browsers()
        if not browsers:
            answer = messagebox.askquestion("Application Mode", "No supported browsers detected. Do you want to use App Mode (Electron)?")
            if answer == 'yes':
                # Start Electron in a separate thread
                electron_thread = threading.Thread(target=open_electron, daemon=True)
                electron_thread.start()
            else:
                messagebox.showinfo("Exit", "No browsers available and Electron mode not selected. Exiting application.")
                sys.exit(0)
        else:
            selected = None

            def on_select(browser_name, browser_path):
                nonlocal selected
                selected = (browser_name, browser_path)
                dialog.destroy()

            dialog = tk.Toplevel()
            dialog.title("Choose Browser or Electron")
            dialog.geometry("500x400")
            os_info = f"Detected OS: {platform.system()} {platform.release()}"
            tk.Label(dialog, text=os_info, font=("Arial", 12)).pack(pady=10)

            # Instructions
            tk.Label(dialog, text="Select a browser to open the application:", font=("Arial", 12)).pack(pady=10)

            # Create buttons for each browser
            for browser_name, browser_path in browsers:
                try:
                    tk.Button(dialog, text=browser_name.capitalize(), width=30,
                              command=lambda b=browser_name, p=browser_path: on_select(b, p)).pack(pady=5)
                except Exception as e:
                    logging.error(f"Failed to create button for {browser_name}: {e}")

            # Button for default browser
            tk.Button(dialog, text="Default Browser", width=30,
                      command=lambda: on_select('default', None)).pack(pady=5)

            # Button for Electron
            tk.Button(dialog, text="Electron App Mode", width=30,
                      command=lambda: on_select('electron', None)).pack(pady=20)

            dialog.mainloop()

            if selected:
                browser_name, browser_path = selected
                if browser_name == 'electron':
                    # Start Electron in a separate thread
                    electron_thread = threading.Thread(target=open_electron, daemon=True)
                    electron_thread.start()
                elif browser_name == 'default':
                    # Start default browser in a separate thread
                    browser_thread = threading.Thread(target=open_default_browser, args=(HOME_URL,), daemon=True)
                    browser_thread.start()
                else:
                    # Start selected browser in a separate thread
                    browser_thread = threading.Thread(target=open_browser, args=(browser_name, browser_path, HOME_URL), daemon=True)
                    browser_thread.start()
    except Exception as e:
        logging.error(f"Error in prompt_user: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def wait_for_flask(url=HOME_URL + HEALTH_ENDPOINT, timeout=10):
    """
    Wait for the Flask server to become available by polling the health endpoint.
    """
    start_time = time.time()
    while True:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    logging.info("Flask server is up and running.")
                    return True
        except Exception as e:
            logging.debug(f"Waiting for Flask server... {e}")
        if time.time() - start_time > timeout:
            logging.error("Timeout waiting for Flask server to start.")
            return False
        time.sleep(0.5)

def start_flask(flask_ready_event):
    """
    Start the Flask server with SocketIO and signal when it's ready.
    """
    try:
        logging.info("Starting Flask server.")

        def run_socketio():
            socketio.run(app, debug=False, port=FLASK_PORT, use_reloader=False)
            logging.info("Flask server stopped.")

        flask_thread = threading.Thread(target=run_socketio)
        flask_thread.start()

        # Wait until the server is up
        if wait_for_flask():
            flask_ready_event.set()
        else:
            flask_ready_event.set()  # Even on failure, set the event to prevent deadlock
    except Exception as e:
        logging.error(f"Failed to start Flask server: {e}")
        flask_ready_event.set()  # Prevent main thread from waiting indefinitely

# ----------------------------
# Flask Routes
# ----------------------------

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering home page: {e}")
        return "Error loading home page", 500

@app.route('/health')
def health():
    return "OK", 200

@app.route('/system_info')
def system_info():
    try:
        data = {
            "os": platform.system(),
            "os_version": platform.version(),
            "browsers": [browser for browser, path in get_installed_browsers()],
            "app_version": app.config.get('APP_VERSION', '1.0.0')
        }
        logging.info("System info retrieved successfully.")
        return jsonify(data)
    except Exception as e:
        logging.error(f"Failed to retrieve system info: {e}")
        return jsonify({"error": "Failed to retrieve system info"}), 500

@app.route('/online')
def online_features_route():
    try:
        if is_connected():
            return jsonify({"status": "online", "message": "You are online! Access AI, search, and video streaming."})
        else:
            return redirect(url_for('offline_route'))
    except Exception as e:
        logging.error(f"Error loading online features: {e}")
        return jsonify({"error": "Error loading online features"}), 500

@app.route('/offline')
def offline_route():
    try:
        return jsonify({"status": "offline", "message": "You are offline! Access local content and offline features."})
    except Exception as e:
        logging.error(f"Error loading offline features: {e}")
        return jsonify({"error": "Error loading offline features"}), 500

# WebSocket event to check online status periodically
@socketio.on('check_online_status')
def handle_check_online_status():
    try:
        status = "online" if is_connected() else "offline"
        emit('online_status', {'status': status})
        logging.info(f"Emitted online status: {status}")
    except Exception as e:
        logging.error(f"Error in WebSocket online status check: {e}")

# ----------------------------
# Main Execution
# ----------------------------

def main():
    """
    Main function to manage threading and user prompt.
    """
    flask_ready_event = threading.Event()

    # Start the Flask server in a background thread
    flask_server_thread = threading.Thread(target=start_flask, args=(flask_ready_event,), daemon=True)
    flask_server_thread.start()
    logging.info("Flask server thread started.")

    # Wait for the Flask server to signal it's ready
    flask_ready_event.wait()
    logging.info("Flask server readiness event received.")

    # Check if Flask server is running
    if is_connected():
        # Prompt the user for the mode (Electron or Browser)
        prompt_user()
    else:
        messagebox.showerror("Error", "Flask server did not start. Exiting application.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        sys.exit(1)
