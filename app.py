from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_current_user, get_jwt_identity, verify_jwt_in_request, create_refresh_token
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
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
from backend.models.appointment import Appointment


# Initialize the Flask application
app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'Quicker-app'

login_manager.login_view = 'login'


app.config['UPLOAD_FOLDER'] = 'static/images'    # new
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} #new
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB  #new



if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite://///Users/alexguadalupe/Documents/GitHub/Portfolio/instance/Quickr.db'   #sqlite:////Users/bags/Portfolio/instance/Quickr.db'
    JWT_SECRET_KEY = 'Quickr-app'


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


@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener el ID del usuario actual
    user_id = current_user.id

    # Obtener las direcciones del usuario
    addresses = Address.query.filter_by(user_id=user_id).all()
    appointments = Appointment.query.filter_by(user_id=user_id).all()

    # Formatear las direcciones para pasarlas a la plantilla
    addresses_data = []
    for address in addresses:
        addresses_data.append({
            'id': address.id,
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'zip_code': address.zip_code,
            'phone': address.phone  # Incluye el teléfono también
        })

    # Formatear las citas para pasarlas a la plantilla
    appointments_data = []
    for appointment in appointments:
        # Suponiendo que appointment_time es un string que representa la hora
        if isinstance(appointment.Appointment_time, str):  # Asegúrate de que es un string
            appointment_time_str = appointment.Appointment_time
            appointment_time = datetime.strptime(appointment_time_str, '%H:%M')  # Convierte a datetime
        else:
            appointment_time = appointment.Appointment_time  # Asumir que ya es un objeto datetime

        appointments_data.append({
            'service_name': appointment.service.name if appointment.service else 'Unknown Service',
            'appointment_date': appointment.Appointment_date.strftime('%B %d, %Y'),  # Formato de fecha
            'appointment_time': appointment_time.strftime('%I:%M %p'),  # Formato de hora AM/PM
            'status': appointment.status
        })

    # Pasar las direcciones y citas formateadas al renderizado de la plantilla
    return render_template('dashboard.html', current_user=current_user, addresses=addresses_data, appointments=appointments_data)



@app.route('/forgot')
def forgot():
    return render_template('forgot.html')



# Profile
@app.route('/profile')
@login_required
def profile():
    user_id = current_user.id

    # Obtener las reseñas del usuario
    reviews = Review.query.filter_by(user_id=user_id).all()

    # Obtener las direcciones del usuario
    addresses = Address.query.filter_by(user_id=user_id).all()

    # Formatear las reseñas para pasarlas a la plantilla
    reviews_data = []
    for review in reviews:
        # Verificar si review.service no es None
        service_name = review.service.name if review.service else "Service not found"
        reviews_data.append({
            'id': review.id,
            'service_id': review.service_id,
            'comment': review.comment,
            'rating': review.rating,
            'service_name': service_name,  # Asignar el nombre del servicio o mensaje de error
            'user': {
                'first_name': review.user.first_name,
                'last_name': review.user.last_name
            }
        })

    # Pasar las direcciones y reseñas a la plantilla
    return render_template('profile.html', current_user=current_user, reviews=reviews_data, addresses=addresses)




# edit profile
@app.route('/profile/user_id', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Si se está simulando un método PUT
    if request.form.get('_method') == 'PUT':
        # Actualizar los datos del usuario
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']
        current_user.phone = request.form.get('phone')

        # Manejar la subida de la imagen de perfil
        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            # Aquí va la lógica para guardar la imagen (ej: en el sistema de archivos o en un servicio de nube)
            # Luego actualiza current_user.profile_pic_url con la URL de la imagen

        # Guardar cambios en la base de datos
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    # Si es un GET, renderiza el formulario de edición
    return render_template('editprofile.html', current_user=current_user)



# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Buscar al usuario en la base de datos
        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"msg": "User not found"}), 401

        # Verificar contraseña
        if not user.check_password(password):
            return jsonify({"msg": "Incorrect password"}), 401

        login_user(user)

        # Generar el token JWT
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)  # Asegúrate de que esto sea un diccionario
        refresh_token = create_refresh_token(identity=user.id)  # Create refresh token

        print("Generated JWT Token:", access_token)

        return jsonify(access_token=access_token, refresh_token=refresh_token, is_admin=user.is_admin), 200

    return render_template('login.html')


# hace refresh al token
@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Verifica que sea un refresh token
def refresh_token():
    current_user_id = get_jwt_identity()  # Obtener la identidad del usuario actual
    access_token = create_access_token(identity=current_user_id)  # Crear un nuevo token de acceso
    return jsonify(access_token=access_token), 200




@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

#logout session
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))  # Redirige al login



# register a user and address
@app.route('/show_register', methods=['GET'])
def show_register():
    return render_template('register.html')

# create user account
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

        login_user(user)

        # Redirigir según el tipo de usuario
        if user_type == 'provider':
            return redirect(url_for('docs'))
        elif user_type == 'client':
            return redirect(url_for('dashboard'))

        return redirect(url_for('dashboard'))

    return render_template('register.html')



# address
@app.route('/addresses/<address_id>', methods=['GET'])
@jwt_required()
def get_address(address_id):
    # Obtener el ID del usuario actual
    current_user = get_jwt_identity()

    # Filtrar por ID de usuario y ID de dirección
    address = Address.query.filter_by(user_id=current_user['id'], id=address_id).first()

    if address:
        address_data = {
            'id': address.id,
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'zip_code': address.zip_code,
            'phone': address.phone
        }
        return jsonify(address_data), 200
    else:
        return jsonify({'message': 'Address not found'}), 404



# SERVICES

# edit service
@app.route('/edit_service/<service_id>', methods=['GET', 'PUT'])
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)

    if request.method == 'GET':
        # Renderiza el formulario con los datos del servicio
        return render_template('edit_service.html', service=service)

    if request.method == 'PUT':
        # Aquí manejas la actualización del servicio
        data = request.get_json()  # Si envías la solicitud como JSON
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.aprox_price = data.get('aprox_price', service.aprox_price)
        service.category = data.get('category', service.category)
        service.fee = data.get('fee', service.fee)

        db.session.commit()
        return jsonify(message='Servicio actualizado con éxito'), 200




# este es para ver todos los servicios en el tab de services.
@app.route('/services/service_id', methods=['GET'])
def get_services():
    # Obtener los parámetros de la consulta
    page = request.args.get('page', 1, type=int)  # Página actual, predeterminada a 1
    per_page = request.args.get('per_page', 10, type=int)  # Servicios por página, predeterminado a 10

    # Obtener los servicios con paginación
    services = Service.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('services.html', services=services)


# Este es para cuadno le das al service entre a la pagina del servicio.
@app.route('/services/<service_id>', methods=['GET', 'POST'])
def review_page(service_id): # service page
    # Obtener el servicio desde la base de datos
    service = Service.query.get(service_id)

    if not service:
        # Si no se encuentra el servicio, devolver un error 404
        abort(404, description="Service not found")

    # Obtener las reseñas asociadas a este servicio
    reviews = Review.query.filter_by(service_id=service_id).all()


    # Pasar el servicio y las reseñas al contexto para renderizar la plantilla
    return render_template('serviceDetails.html', service=service, reviews=reviews)



#@app.route('/services/<service_id>/reviews', methods=['GET'])
#def get_reviews(service_id):
#    reviews = Review.query.filter_by(service_id=service_id).all()
#    return render_template('serviceDetails.html', reviews=reviews)


# esto es para crear reviews en la pagina del servicio. (si esta logged in)
@app.route('/services/<service_id>/reviews', methods=['POST'])
@login_required  # Asegúrate de que el usuario esté autenticado
def create_review(service_id):
    data = request.get_json()
    comment = data.get('comment')
    rating = data.get('rating')

    # Aquí puedes agregar la lógica para crear la reseña
    review = Review(
        service_id=service_id,
        user_id=current_user.id,  # Usa el ID del usuario actualmente autenticado
        comment=comment,
        rating=rating
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({"msg": "Review submitted successfully!"}), 201



@app.route('/users/<user_id>/reviews', methods=['GET'])
@jwt_required()
def get_user_reviews(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:  # Asegúrate de que el usuario está autenticado para ver sus reseñas
        return jsonify({"msg": "Unauthorized"}), 403

    reviews = Review.query.filter_by(user_id=user_id).all()

    # Formatear las reseñas para la respuesta
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'id': review.id,
            'service_id': review.service_id,
            'comment': review.comment,
            'rating': review.rating,
            'user': {
                'first_name': review.user.first_name,  # Asegúrate de que el modelo de usuario tiene estos campos
                'last_name': review.user.last_name
            }
        })

    return jsonify(reviews_data), 200



# paginas regulares

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

@app.route('/docs')
def docs():
    return render_template('docs.html')






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