from flask import Flask
from my_new_app.extensions import db, migrate, bcrypt

app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Make sure this is set

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

# Import routes at the bottom to avoid circular imports
from my_new_app import routes