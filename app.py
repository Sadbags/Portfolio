from flask import Flask, render_template, request, redirect, url_for
import os
from backend.database import db
from backend.Apis.user_endpoint import user_blueprint
from backend.Apis.review_endpoint import review_blueprint
from backend.Apis.appointments_endpoint import appointments_blueprint
from backend.Apis.service_endpoint import service_blueprint
from backend.Apis.address_endpoint import address_blueprint


# Initialize the Flask application
app = Flask(__name__)

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

# Define the route for the default URL, which is the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home1():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

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
