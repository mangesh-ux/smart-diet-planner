"""main.py"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask app
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_diet_plan_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Import routes after app is created to avoid circular import
from smart_diet_plan_app import routes
