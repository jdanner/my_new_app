from flask import Flask
from my_new_app.extensions import db, migrate, bcrypt, login_manager
import os

app = Flask(__name__)

# Configure the app
if os.environ.get('RENDER'):
    # Use the mounted disk directory
    db_path = '/var/data/site.db'
    os.makedirs('/var/data', exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"Using database at: {db_path}")
    print(f"Directory exists: {os.path.exists('/var/data')}")
    print(f"Directory writable: {os.access('/var/data', os.W_OK)}")
else:
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

# Import models to register them with SQLAlchemy
from my_new_app.models import User, Workout, Exercise, ExerciseType

# Import routes at the bottom
from my_new_app import routes