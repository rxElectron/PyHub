# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# Copyright 2024    PyHub/app/live_console/routes.py 

from . import live_console
from flask import render_template

# @live_console.route('/live_console')
# def live_console_page():
#     return render_template('live_console.html')

# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# app/live_console/routes.py
from flask import Blueprint, request, jsonify, render_template
import sys , io , contextlib , logging , os
from pathlib import Path
import datetime

allowed_builtins = {
    'print': print,
    'range': range,
    'len': len,
    # Add other safe built-ins
}

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
        with open(file_path, 'w') as f:
            f.write(code)
        logging.info(f"Code saved to {file_path}")
        return jsonify({'status': 'success', 'filename': filename})
    except Exception as e:
        logging.error(f"Failed to save code: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save code.'}), 500
