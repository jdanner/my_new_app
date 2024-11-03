#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
export FLASK_APP=wsgi.py
flask db upgrade