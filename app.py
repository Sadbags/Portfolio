from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
import os

# Blueprint imports
from backend.database import db
from backend.Apis.user_endpoint import user_blueprint
from backend.Apis.review_endpoint import review_blueprint
from backend.Apis.appointments_endpoint import appointments_blueprint
from backend.Apis.service_endpoint import service_blueprint
from backend.Apis.address_endpoint import address_blueprint
from backend.Apis.docs_endpoint import docs_blueprint
from backend.Apis.files_endpoint import files_blueprint
#from backend.Apis.register_endpoint import register_blueprint

# model imports
from backend.models.user import User
from backend.models.address import Address


# Initialize the Flask application
app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)
app.secret_key = 'Quicker-app'

class Config(object):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bags/Portfolio/instance/Quickr.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret'


class DevelopmentConfig(Config):
	DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

environment_config = DevelopmentConfig if os.environ.get(
	'ENV') == 'Quickr' else ProductionConfig
app.config.from_object(environment_config)

db.init_app(app)
jwt = JWTManager(app)

# Define the route for the default URL, which is the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home1():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario de inicio de sesión desde JSON
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Aquí puedes agregar la lógica para autenticar al usuario
        user = User.query.filter_by(email=email).first()

        if user is None:
            abort(401, description='User not found')

        if not user.check_password(password):
            abort(401, description='Incorrect password')

        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200

    return render_template('login.html')


# register a user and address

@app.route('/show_register', methods=['GET'])
def show_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        # Obtener los datos enviados en formato JSON
        data = request.get_json()

        # Obtener los datos del formulario desde el JSON
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        user_type = data.get('user_type')

        # Validación básica de contraseña
        if not password or not confirm_password:
            return jsonify({"error": "Password cannot be empty"}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        # Hash de la contraseña

        # Crear el usuario con is_admin como False por defecto
        user = User(
            email=email,
            password=request.json.get('password'),
            first_name=request.json.get('first_name'),
            last_name=request.json.get('last_name'),
            is_admin=request.json.get('is_admin', False),
        )
        db.session.add(user)
        db.session.commit()

        # Obtener los datos de la dirección
        address = data.get('address')
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code')
        phone = data.get('phone')

        # Crear la dirección
        address = Address(
            address=address,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            user_id=user.id
        )
        db.session.add(address)
        db.session.commit()



        # Redirigir según el tipo de usuario
        if user_type == 'provider':
            return redirect(url_for('docs'))
        elif user_type == 'client':
            return redirect(url_for('dashboard'))

        return redirect(url_for('dashboard'))

    return render_template('register.html')







@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')



@app.route('/docs')
def docs():
    return render_template('docs.html')


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
app.register_blueprint(docs_blueprint)
app.register_blueprint(files_blueprint)
#app.register_blueprint(register_blueprint)

with app.app_context():
	db.create_all()

# Runs the application
if __name__ == '__main__':
	app.run(debug=True)