# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# Copyright 2024    PyHub/config.py 

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variables for better security
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database/offline_db.sqlite')  # Flexible for different environments
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False  # Disable debug mode in production for better performance
