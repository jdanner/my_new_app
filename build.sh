#!/usr/bin/env bash
# Make script executable: chmod +x build.sh

# Install Python dependencies
pip install -r requirements.txt

# Create the database tables first
python init_db.py

# Then run migrations
export FLASK_APP=wsgi.py
flask db stamp head  # Mark current migration as complete
flask db upgrade    # Run any pending migrations

# You might also want to add any other build steps here