from my_new_app import app
from my_new_app.extensions import db

with app.app_context():
    db.create_all()