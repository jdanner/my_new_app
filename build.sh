#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Just run migrations - this will create tables too
export FLASK_APP=wsgi.py
flask db upgrade