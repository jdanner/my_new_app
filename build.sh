#!/usr/bin/env bash
# Make script executable: chmod +x build.sh

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# You might also want to add any other build steps here