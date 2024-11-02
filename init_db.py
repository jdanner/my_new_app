from my_new_app import app
from my_new_app.extensions import db
from my_new_app.models import User

with app.app_context():
    db.create_all()
    
    # Create a test user if it doesn't exist
    if not User.query.filter_by(email='test@test.com').first():
        user = User(
            username='test',
            email='test@test.com',
            password='test'  # Don't do this in production!
        )
        db.session.add(user)
        db.session.commit()
        print("Test user created!")