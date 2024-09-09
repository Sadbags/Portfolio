from flask import Flask
from flask_migrate import Migrate
import os
from database import db
from Apis.user_endpoint import user_blueprint
from Apis.review_endpoint import review_blueprint
from Apis.appointments_endpoint import appointments_blueprint
from Apis.service_endpoint import service_blueprint
from Apis.address_endpoint import address_blueprint


# Initialize the Flask application
app = Flask(__name__)
migrate = Migrate(app, db)


class Config(object):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Quickr.db'
    JWT_SECRET_KEY = 'super-secret'


class DevelopmentConfig(Config):
	DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

environment_config = DevelopmentConfig if os.environ.get(
	'ENV') == 'Quickr' else ProductionConfig
app.config.from_object(environment_config)

db.init_app(app)

# Define a route for the home page
@app.route('/')
def home():
	return 'Welcome to quickr'

app.register_blueprint(user_blueprint)
app.register_blueprint(review_blueprint)
app.register_blueprint(appointments_blueprint)
app.register_blueprint(service_blueprint)
app.register_blueprint(address_blueprint)

with app.app_context():
	db.create_all()

# Runs the application
if __name__ == '__main__':
	app.run(debug=True)
