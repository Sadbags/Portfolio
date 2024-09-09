from flask import Blueprint, request, jsonify, abort
from models.user import User
from models.address import Address
from database import db


user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/users', methods=['POST'])
def login():
    data = request.get.json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid email or password'}), 401
    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200


@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Crear el nuevo usuario
    user = User(
        email=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        is_admin=data.get('is_admin')
    )

    # Agregar el usuario a la base de datos
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200



@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify(user.to_dict()), 200


@user_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
	user = User.query.get(user_id)
	if not user:
		return jsonify({'error': 'Usuario no encontrado'}), 404

	data = request.get_json()

	user.email = data.get('email', user.email)
	user.first_name = data.get('first_name', user.first_name)
	user.last_name = data.get('last_name', user.last_name)
	user.password = data.get('password', user.password)

	db.session.commit()

	return jsonify(user.to_dict()), 200


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	user = User.query.get(user_id)
	if not user:
		return jsonify({'error': 'Usuario no encontrado'}), 404

	db.session.delete(user)
	db.session.commit()

	return '', 204
