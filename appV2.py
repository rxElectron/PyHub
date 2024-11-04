import socket
import threading
import platform
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import logging
import os
import time
import urllib.request

# تنظیمات Logging با فرمت زمان‌بندی شده
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask app and SocketIO
app = Flask(__name__)
try:
    socketio = SocketIO(app)
    logging.info("SocketIO initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize SocketIO: {e}")

# Load configurations from config.py
try:
    app.config.from_object('config.Config')
    logging.info("Configurations loaded from config.py")
except Exception as e:
    logging.error(f"Failed to load configurations: {e}")

# Register blueprints
try:
    from app.debug.routes import debug_bp
    from app.explore.routes import explore_bp
    from app.code_comparator.routes import comparator_bp
    from app.learning.routes import learning_bp
    from app.live_console.routes import live_console_bp
    from app.profile.routes import profile_bp
    from app.project_manager.routes import project_manager_bp
    from app.settings.routes import settings_bp
    from app.video.routes import video_bp

    app.register_blueprint(debug_bp)
    app.register_blueprint(explore_bp)
    app.register_blueprint(comparator_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(live_console_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(project_manager_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(video_bp)
    logging.info("All blueprints registered successfully.")
except ImportError as e:
    logging.error(f"Failed to register blueprints: {e}")

# Function to check internet connection
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.create_connection((host, port), timeout=timeout)
        logging.info("Internet connection is available.")
        return True
    except OSError as e:
        logging.warning(f"No internet connection: {e}")
        return False

# Function to wait for Flask server to start
def wait_for_flask(url='http://127.0.0.1:5000/', timeout=10):
    start_time = time.time()
    while True:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    logging.info("Flask server is up and running.")
                    return True
        except Exception:
            pass
        if time.time() - start_time > timeout:
            logging.error("Timeout waiting for Flask server to start.")
            return False
        time.sleep(0.5)

# Function to get installed browsers based on OS with exception handling
def get_installed_browsers():
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

        for browser, path in paths.items():
            try:
                if platform.system() == "Linux":
                    # For Linux, check if the browser is in PATH
                    if subprocess.run(["which", browser], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        browsers.append((browser, browser))  # browser name and command
                        logging.info(f"{browser} detected in PATH.")
                else:
                    # For Windows and macOS, check if the executable exists
                    if os.path.exists(path):
                        browsers.append((browser, path))  # browser name and path
                        logging.info(f"{browser} detected at {path}.")
            except Exception as e:
                logging.error(f"Failed to check browser {browser}: {e}")
    except Exception as e:
        logging.error(f"Failed to detect installed browsers: {e}")
    return browsers

# Function to open a specific browser with exception handling
def open_browser(browser_name, browser_path, url):
    try:
        logging.info(f"Attempting to open {browser_name} with URL: {url}")
        if platform.system() == "Windows":
            subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Linux":
            subprocess.Popen([browser_path, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"{browser_name.capitalize()} browser opened successfully with URL: {url}")
    except Exception as e:
        logging.error(f"Failed to open {browser_name}: {e}")
        messagebox.showerror("Browser Error", f"Failed to open {browser_name}: {e}")
        # Optionally, prompt to use Electron
        if messagebox.askyesno("Open Electron", f"Do you want to open the application in Electron instead of {browser_name}?"):
            open_electron()
        else:
            logging.info("User chose not to open Electron.")

# Function to open default browser with exception handling
def open_default_browser(url):
    try:
        logging.info(f"Attempting to open default browser with URL: {url}")
        webbrowser.open(url)
        logging.info(f"Default browser opened successfully with URL: {url}")
    except Exception as e:
        logging.error(f"Failed to open default browser: {e}")
        messagebox.showerror("Browser Error", f"Failed to open default browser: {e}")
        if messagebox.askyesno("Open Electron", "Do you want to open the application in Electron instead of the default browser?"):
            open_electron()
        else:
            logging.info("User chose not to open Electron.")

# Function to open Electron app with exception handling
def open_electron():
    try:
        logging.info("Attempting to start Electron app.")
        electron_dir = os.path.join(os.path.dirname(__file__), 'electron_app')
        # Use subprocess.Popen to start Electron asynchronously
        # Assuming package.json has the correct start script
        process = subprocess.Popen(['npm', 'start'], cwd=electron_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Electron app started successfully.")
    except Exception as e:
        logging.error(f"Failed to start Electron: {e}")
        messagebox.showerror("Error", f"Failed to start Electron: {e}")

# Define route to serve the home page
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering home page: {e}")
        return "Error loading home page"

# Route to serve system info
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
        return jsonify({"error": "Failed to retrieve system info"})

# WebSocket event to check online status periodically
@socketio.on('check_online_status')
def handle_check_online_status():
    try:
        status = "online" if is_connected() else "offline"
        emit('online_status', {'status': status})
        logging.info(f"Emitted online status: {status}")
    except Exception as e:
        logging.error(f"Error in WebSocket online status check: {e}")

# Route for online features
@app.route('/online')
def online_features_route():
    try:
        if is_connected():
            return jsonify({"status": "online", "message": "You are online! Access AI, search, and video streaming."})
        else:
            return redirect(url_for('offline_route'))
    except Exception as e:
        logging.error(f"Error loading online features: {e}")
        return jsonify({"error": "Error loading online features"})

# Route for offline features
@app.route('/offline')
def offline_route():
    try:
        return jsonify({"status": "offline", "message": "You are offline! Access local content and offline features."})
    except Exception as e:
        logging.error(f"Error loading offline features: {e}")
        return jsonify({"error": "Error loading offline features"})

# Function to prompt the user with a GUI for Browser or Electron with exception handling
def prompt_user():
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
                os._exit(0)
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
                    browser_thread = threading.Thread(target=open_default_browser, args=('http://127.0.0.1:5000/',), daemon=True)
                    browser_thread.start()
                else:
                    # Start selected browser in a separate thread
                    browser_thread = threading.Thread(target=open_browser, args=(browser_name, browser_path, 'http://127.0.0.1:5000/'), daemon=True)
                    browser_thread.start()
    except Exception as e:
        logging.error(f"Error in prompt_user: {e}")

# Start Flask server in a separate thread with exception handling
def start_flask():
    try:
        logging.info("Starting Flask server.")
        socketio.run(app, debug=False, port=5000, use_reloader=False)
        logging.info("Flask server started.")
    except Exception as e:
        logging.error(f"Failed to start Flask server: {e}")

if __name__ == "__main__":
    try:
        # Start the Flask server in a background thread
        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()
        logging.info("Flask server thread started.")

        # Wait for Flask server to start by checking connectivity to Flask URL
        if wait_for_flask():
            # Prompt the user for the mode (Electron or Browser)
            prompt_user()
        else:
            messagebox.showerror("Error", "Flask server did not start. Exiting application.")
            os._exit(1)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
