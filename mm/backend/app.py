# backend/app.py

from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp
from flask_migrate import Migrate

app = Flask(__name__)

# CORS setup
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

# PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9600847958$@localhost/test_mlt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Register the routes blueprint
app.register_blueprint(bp)



# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
