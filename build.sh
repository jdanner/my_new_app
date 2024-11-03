#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Create a temporary Python script to create tables
cat << EOF > create_tables.py
from my_new_app import app
from my_new_app.extensions import db
from my_new_app.models import Exercise  # Import your models

with app.app_context():
    db.create_all()
    # Add initial exercise if it doesn't exist
    exercise = Exercise.query.filter_by(exercise_type='Bench Press').first()
    if not exercise:
        new_exercise = Exercise(exercise_type='Bench Press')
        db.session.add(new_exercise)
        db.session.commit()
EOF

# Create tables and initial data
python create_tables.py

# Now run migrations
export FLASK_APP=wsgi.py
flask db stamp head  # Mark current migration as complete
flask db upgrade    # Run any pending migrations