from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from backend.models.user import User
from backend.models.address import Address
from backend.database import db


user_blueprint = Blueprint('user_blueprint', __name__)

#@user_blueprint.route('/api/register', methods=['POST'])
#def register():
#    if not request.json:
#        abort(400, description='Missing JSON data')
#
    # Obtener los datos del usuario
#    first_name = request.json.get('first_name')
#    last_name = request.json.get('last_name')
#    email = request.json.get('email')
#    password = request.json.get('password')
#    confirm_password = request.json.get('confirm-password')
#    user_type = request.json.get('user_type')

    # Verificación de datos básicos
 #   if not email or not password or not confirm_password:
#        abort(400, description="Missing email or password")

#    if password != confirm_password:
#        abort(400, description="Passwords do not match")

 #   # Crear el usuario
 #   user = User(
 #       first_name=first_name,
 #       last_name=last_name,
 #       email=email,
 #       password=password,  # Nota: Asegúrate de que la contraseña esté encriptada
  #      user_type=user_type
  #  )

  #  db.session.add(user)
  #  db.session.commit()  # Guardar el usuario primero para obtener el user_id

    # Obtener los datos de dirección
  #  street = request.json.get('street')
  #  city = request.json.get('city')
  #  state = request.json.get('state')
  #  phone = request.json.get('phone')
  #  zip_code = request.json.get('zip_code')
  #  country = request.json.get('country')

    # Crear la dirección
  #  address = Address(
  #      street=street,
  #      city=city,
  #      state=state,
  #      phone=phone,
  #      zip_code=zip_code,
  #      country=country,
  #      user_id=user.id  # Asocia la dirección al usuario creado
  #  )

  #  db.session.add(address)
  #  db.session.commit()  # Guardar la dirección en la base de datos

  #  return jsonify({"msg": "User and address created successfully", "user_id": user.id}), 201

@user_blueprint.route('/users/<user_id>/profile_picture', methods=['POST'])
def upload_profile_picture(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'profile_picture' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['profile_picture']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        user.set_profile_picture(file)  # Método para guardar la imagen en la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos

        # Devuelve un mensaje y la nueva imagen en base64
        return jsonify({"message": "Profile picture uploaded successfully", "profile_picture": user.profile_picture}), 200

    return jsonify({"error": "File upload failed"}), 500

@user_blueprint.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        abort(404, description="User not found")

    if user.is_admin:
        return jsonify(message=f"Welcome, admin {user.first_name}.", user_details={"id": user.id, "email": user.email}), 200
    else:
        return jsonify(message=f"Welcome, regular user {user.first_name}.", user_details={"id": user.id, "email": user.email}), 200


@user_blueprint.route('/api/login', methods=['POST'])
def login():
    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400, description='Missing required fields')

    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()

    if user is None:
        abort(401, description='User not found')

    if not user.check_password(password):
        abort(401, description='Incorrect password')

    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify(access_token=access_token), 200


@user_blueprint.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    claims = get_jwt()  # Use get_jwt() to get additional claims like is_admin

    # Now check if the user is admin
    if not claims.get('is_admin'):
        abort(403, description='Admin rights required')

    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400, description='Missing required fields')

    email = request.json.get('email')
    if '@' not in email:
        abort(400, description='Invalid email format')

    password = request.json.get('password')
    if password is None:
        abort(400, description='Password is required')

    user = User(
        email=email,
        password=request.json.get('password'),
        first_name=request.json.get('first_name'),
        last_name=request.json.get('last_name'),
        is_admin=request.json.get('is_admin', False)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully", "user_id": user.id}), 201



@user_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.get(get_jwt_identity())

    if not User.is_admin:
        abort(403, description='Admin rights required')

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200



@user_blueprint.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    claims = get_jwt()  # Use get_jwt() to get additional claims like is_admin
    if not claims.get('is_admin'):
        abort(403, description='Admin rights required')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify(user.to_dict()), 200



@user_blueprint.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)

    if user is None:
        abort(404, description="User not found")

    if not current_user.is_admin and current_user_id != user_id:
        abort(403, description="You do not have permission to update this user")

    data = request.get_json()

    if 'email' in data:
        user.email = data['email']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        user.password = data['password']

    db.session.commit()

    return jsonify({"msg": "User updated successfully", "user": user.to_dict()}), 200


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)

    if user is None:
        abort(404, description="User not found")

    if not current_user.is_admin and current_user_id != user_id:
        abort(403, description="You do not have permission to delete this user")

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200
