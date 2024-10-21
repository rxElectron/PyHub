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

# Initialize the Flask app
app = Flask(__name__)

# Load configurations from config.py
app.config.from_object('config.Config')

# Register blueprints (assuming they are properly defined in your app folder)
from app.debug.routes import debug_bp
from app.explore.routes import explore_bp

app.register_blueprint(debug_bp)
app.register_blueprint(explore_bp)

# Function to check internet connection
def is_connected(host="1.1.1.1", port=53, timeout=3):
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False

# Define a route to serve the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for online features (activated only if connected)
@app.route('/online')
def online_features():
    if is_connected():
        return jsonify({"status": "online", "message": "You are online! Access AI, search, and video streaming."})
    else:
        return redirect(url_for('offline'))

# Route for offline features (always accessible)
@app.route('/offline')
def offline():
    return jsonify({"status": "offline", "message": "You are offline! Access local content and offline features."})

# Start Flask server in a separate thread
def start_flask():
    try:
        app.run(debug=False, port=5000, use_reloader=False)
    except Exception as e:
        logging.error(f"Failed to start Flask: {e}")

# Function to open Electron app
def open_electron():
    # Ensure you're in the electron_app directory
    electron_dir = os.path.join(os.path.dirname(__file__), 'electron_app')
    
    # Run Electron via npm start
    subprocess.run(['yarn', 'start'], cwd=electron_dir)

# Function to prompt the user with a GUI for WebView or browser
def prompt_user():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user if they want to use Electron or Browser
    answer = messagebox.askquestion("Application Mode", "Do you want to use the App Mode (Electron)?")

    if answer == 'yes':
        open_electron()  # Launch Electron instead of WebView
    else:
        webbrowser.open('http://127.0.0.1:5000/')  # Fallback to browser mode

if __name__ == "__main__":
    # Start the Flask server in a background thread
    threading.Thread(target=start_flask).start()

    # Prompt the user for the mode (Electron or Browser)
    prompt_user()
