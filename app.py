from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
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
from backend.models.service import Service
from backend.models.review import Review


# Initialize the Flask application
app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'Quicker-app'

login_manager.login_view = 'login'


app.config['UPLOAD_FOLDER'] = 'uploads'    # new
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} #new
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB  #new

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Config(object):  # 'sqlite:////Users/bags/Portfolio/instance/Quickr.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bgarc/VsCode/Portfolio/instance/Quickr.db'
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

# Define the route for the dashboard
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
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"msg": "User not found"}), 401

        if not user.check_password(password):
            return jsonify({"msg": "Incorrect password"}), 401

        # Aquí llamamos a login_user para iniciar sesión
        login_user(user)

        # Devolvemos un JSON con la URL de redirección en vez de usar 'redirect'
        return jsonify({"msg": "Login successful", "redirect_url": url_for('profile')}), 200

    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/profile')
@login_required
def profile():
    print(current_user.is_authenticated)  # Esto debería imprimir True
    return render_template('profile.html', current_user=current_user)


# Edit Profile route
@app.route('/edit_profile')
def edit_profile():
    return render_template('editprofile.html')




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











@app.route('/docs')
def docs():
    return render_template('docs.html')




@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return render_template('services.html', services=services)


@app.route('/services')
def services_page():
    services = get_services()  # Esta función debe devolver una lista de servicios
    return render_template('services.html', services=services)


@app.route('/services/<service_id>', methods=['GET', 'POST'])
def review_page(service_id):
    # Obtener el servicio desde la base de datos
    service = Service.query.get(service_id)

    if service is None:
        # Si no se encuentra el servicio, devolver un error 404
        return jsonify({"error": "Service not found"}), 404

    # Obtener las reseñas asociadas a este servicio
    reviews = Review.query.filter_by(service_id=service_id).all()

    # Pasar el servicio y las reseñas al contexto para renderizar la plantilla
    return render_template('reviews.html', service=service, reviews=reviews)



@app.route('/services/<service_id>/reviews', methods=['GET'])
def get_reviews(service_id):
    reviews = Review.query.filter_by(service_id=service_id).all()
    return render_template('reviews.html', reviews=reviews)





@app.route('/submit_review', methods=['POST'])
@login_required  # Esto asegura que solo los usuarios autenticados puedan dejar reseñas
def submit_review():
    if request.is_json:
        # Si los datos vienen como JSON, los obtenemos con request.get_json()
        data = request.get_json()
        service_id = data.get('service_id')
        comment = data.get('comment')
        rating = data.get('rating')
    else:
        # Si los datos vienen de un formulario, los obtenemos con request.form
        service_id = request.form.get('service_id')
        comment = request.form.get('comment')
        rating = request.form.get('rating')

    # Obtener el usuario actual
    user_id = current_user.id  # current_user viene de flask_login

    # Crear la nueva reseña (instancia del modelo Review)
    new_review = Review(service_id=service_id, user_id=user_id, comment=comment, rating=rating)

    # Guardar la reseña en la base de datos
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Hacemos rollback en caso de error
        return jsonify({"message": "An error occurred while saving the review", "error": str(e)}), 500








@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')


@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')













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