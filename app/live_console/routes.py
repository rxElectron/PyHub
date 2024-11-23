# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# Copyright 2024    PyHub/app/live_console/routes.py 

from flask import Blueprint, jsonify, request
from flask_socketio import Namespace, emit
import subprocess, threading, logging 
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from flask_socketio import SocketIO, emit

from . import live_console
from flask import render_template

@live_console.route('/live_console')
def live_console_page():
    return render_template('live_console.html')

# @live_console.route('/live_console')
# def live_console_page():
#     return render_template('live_console.html')

# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# app/live_console/routes.py# app/live_console/routes.py

from flask import Blueprint, request, jsonify, render_template
import sys , io , contextlib , logging , os
from pathlib import Path
import datetime
import base64

# Initialize Blueprint
live_console = Blueprint('live_console', __name__)

# Logger Configuration
logger = logging.getLogger(__name__)

# Define Allowed Built-ins for RestrictedPython
allowed_builtins = {
    'print': print,
    'range': range,
    'len': len,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # Add other safe built-ins as needed
}

# Flask Routes

@live_console.route('/live_console')
def live_console_page():
    return render_template('live_console.html')

@live_console.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')

    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {'__builtins__': allowed_builtins}, {})
        output = stdout.getvalue()
    except Exception as e:
        output = str(e)

    return jsonify({'output': output})

@live_console.route('/save_code', methods=['POST'])
def save_code():
    data = request.get_json()
    code = data.get('code', '')

    # Define the directory to save code
    saved_codes_dir = Path(__file__).parent.parent.parent / 'saved_codes'
    saved_codes_dir.mkdir(exist_ok=True)

    # Create a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"saved_code_{timestamp}.py"
    file_path = saved_codes_dir / filename

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        logger.info(f"Code saved to {file_path}")
        return jsonify({'status': 'success', 'filename': filename})
    except Exception as e:
        logger.error(f"Failed to save code: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save code.'}), 500

@live_console.route('/list_codes', methods=['GET'])
def list_codes():
    saved_codes_dir = Path(__file__).parent.parent.parent / 'saved_codes'
    if not saved_codes_dir.exists():
        return jsonify({'status': 'success', 'files': []})

    files = [f.name for f in saved_codes_dir.glob("*.py")]
    return jsonify({'status': 'success', 'files': files})

@live_console.route('/load_code', methods=['GET'])
def load_code():
    filename = request.args.get('filename', '')
    saved_codes_dir = Path(__file__).parent.parent.parent / 'saved_codes'
    file_path = saved_codes_dir / filename

    if not file_path.exists():
        return jsonify({'status': 'error', 'message': 'File not found.'}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return jsonify({'status': 'success', 'code': code})
    except Exception as e:
        logger.error(f"Failed to load code: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to load code.'}), 500

@live_console.route('/load_file', methods=['GET'])
def load_file():
    filename = request.args.get('filename', '')
    saved_codes_dir = Path(__file__).parent.parent.parent / 'saved_codes'
    file_path = saved_codes_dir / filename

    if not file_path.exists():
        return jsonify({'status': 'error', 'message': 'File not found.'}), 404

    try:
        file_extension = file_path.suffix.lower()
        if file_extension in ['.png', '.jpg', '.jpeg', '.gif']:
            with open(file_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')
            return jsonify({'status': 'success', 'type': 'image', 'data': encoded_image})
        elif file_extension == '.pdf':
            with open(file_path, 'rb') as f:
                encoded_pdf = base64.b64encode(f.read()).decode('utf-8')
            return jsonify({'status': 'success', 'type': 'pdf', 'data': encoded_pdf})
        elif file_extension in ['.txt', '.md', '.py']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'status': 'success', 'type': 'text', 'data': content})
        else:
            return jsonify({'status': 'error', 'message': 'Unsupported file type.'}), 400
    except Exception as e:
        logger.error(f"Failed to load file: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to load file.'}), 500

# Socket.IO Namespaces

class PythonConsoleNamespace(Namespace):
    def on_connect(self):
        logger.info("Client connected to Python Console namespace.")

    def on_disconnect(self):
        logger.info("Client disconnected from Python Console namespace.")

    def on_execute_code(self, data):
        code = data.get('code', '')
        logger.info(f"Executing Python code: {code}")

        # Restrict the execution environment
        restricted_globals = {
            '__builtins__': safe_builtins,
            '_print_': print,
        }
        restricted_locals = {}

        stdout = io.StringIO()
        try:
            byte_code = compile_restricted(code, '<string>', 'exec')
            with contextlib.redirect_stdout(stdout):
                exec(byte_code, restricted_globals, restricted_locals)
            output = stdout.getvalue()
            emit('execution_result', {'output': output})
        except Exception as e:
            output = f"{type(e).__name__}: {e}"
            emit('execution_result', {'output': output})

class TerminalNamespace(Namespace):
    def on_connect(self):
        logger.info("Client connected to Terminal namespace.")
        self.process = None
        self.thread = None

    def on_disconnect(self):
        logger.info("Client disconnected from Terminal namespace.")
        if self.process:
            self.process.terminate()
            self.process = None
        if self.thread and self.thread.is_alive():
            self.thread.join()
            self.thread = None

    def on_start_terminal(self):
        if self.process:
            emit("terminal_output", "Terminal is already running.\n")
            return

        # Determine shell based on OS
        shell = True if sys.platform.startswith('win') else False
        shell_command = "cmd.exe" if sys.platform.startswith('win') else "/bin/bash"

        try:
            self.process = subprocess.Popen(
                shell_command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            # Start a thread to read output
            self.thread = threading.Thread(target=self.read_output)
            self.thread.start()
            emit("terminal_output", f"Started {shell_command}.\n")
        except Exception as e:
            emit("terminal_output", f"Error starting terminal: {e}\n")

    def on_start_python(self):
        if self.process:
            emit("terminal_output", "A process is already running.\n")
            return

        # Start Python interpreter
        python_command = "python" if sys.platform.startswith('win') else "python3"

        try:
            self.process = subprocess.Popen(
                [python_command],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            # Start a thread to read output
            self.thread = threading.Thread(target=self.read_output)
            self.thread.start()
            emit("terminal_output", f"Started Python interpreter.\n")
        except Exception as e:
            emit("terminal_output", f"Error starting Python: {e}\n")

    def on_execute_command(self, data):
        command = data.get('command', '')
        if self.process:
            try:
                self.process.stdin.write(command + '\n')
                self.process.stdin.flush()
            except Exception as e:
                emit("terminal_output", f"Error sending command: {e}\n")
        else:
            emit("terminal_output", "No active process.\n")

    def read_output(self):
        try:
            while True:
                output = self.process.stdout.readline()
                if output:
                    emit('terminal_output', output)
                else:
                    break
            # Read remaining stderr
            stderr = self.process.stderr.read()
            if stderr:
                emit('terminal_output', stderr)
        except Exception as e:
            emit('terminal_output', f"Error reading output: {e}\n")
        finally:
            if self.process:
                self.process.terminate()
                self.process = None
            emit('terminal_output', "Process terminated.\n")

# Register Namespaces Function
def register_socketio_namespaces(socketio):
    socketio.on_namespace(PythonConsoleNamespace('/python_console'))
    socketio.on_namespace(TerminalNamespace('/terminal'))

# Register Namespaces
def setup_socketio_namespaces(socketio):
    register_socketio_namespaces(socketio)
