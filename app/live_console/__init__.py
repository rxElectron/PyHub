# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# Copyright 2024    PyHub/app/live_console/__init__.py 

from flask import Blueprint

live_console = Blueprint('live_console', __name__)

from . import routes

# ----------------------------------------------------------------
