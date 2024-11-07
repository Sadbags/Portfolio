from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models.service import Service
from backend.database import db

import base64   #new
import requests  #new
from io import BytesIO  #new
from PIL import Image #new

service_blueprint = Blueprint('service_blueprint', __name__)


@service_blueprint.route('/api/services', methods=['POST'])
@jwt_required()
def create_service():
    current_user_id = get_jwt_identity()

    # Validar que el cuerpo de la solicitud JSON tenga todos los campos requeridos
    required_fields = ['name', 'description', 'aprox_price', 'category', 'fee', 'picture']
    if not request.json or not all(key in request.json for key in required_fields):
        abort(400, description="Missing required fields")

    # Obtener datos de la solicitud
    name = request.json['name']
    description = request.json['description']
    aprox_price = request.json['aprox_price']
    category = request.json['category']
    fee = request.json['fee']
    picture_data = request.json['picture']  # Obtener la imagen del servicio

    # Crear la instancia de Service
    service = Service(
        name=name,
        description=description,
        aprox_price=aprox_price,
        category=category,
        fee=fee,
        user_id=current_user_id
    )

    # Asignar la imagen directamente desde el string base64
    service.picture = picture_data

    # Agregar el servicio a la sesión de la base de datos y hacer commit
    db.session.add(service)
    db.session.commit()

    # Retornar el servicio creado en formato JSON
    return jsonify(service.to_dict()), 201






@service_blueprint.route('/api/services', methods=['GET'])
def get_services():
	services = Service.query.all()

	return jsonify([service.to_dict() for service in services]), 200


@service_blueprint.route('/api/services/<service_id>', methods=['GET'])
def get_service(service_id):
	service = Service.query.get(service_id)

	if service is None:
		abort(404, description="Service not found")

	return jsonify(service.to_dict()), 200

@service_blueprint.route('/services/<service_id>/appointments', methods=['GET'])
@jwt_required()
def get_appointments_by_service(service_id):
    # Obtener el ID del usuario autenticado desde el token JWT (opcional si solo quieres mostrar citas para usuarios autenticados)
    current_user_id = get_jwt_identity()

    # Obtener todas las citas para el servicio dado
    appointments_query = Appointment.query.filter_by(service_id=service_id).all()

    # Si no se encuentran citas para ese servicio, devolver un error 404
    if not appointments_query:
        abort(404, description="No appointments found for the given service")

    # Convertir las citas a formato dict
    appointments_list = [appointment.to_dict() for appointment in appointments_query]

    # Retornar la lista de citas en formato JSON
    return jsonify(appointments_list), 200





@service_blueprint.route('/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)

    if service is None:
        abort(404, description="Service not found")

    data = request.json

    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.aprox_price = data.get('aprox_price', service.aprox_price)
    service.category = data.get('category', service.category)
    service.fee = data.get('fee', service.fee)
    service.img_url = data.get('img_url', service.img_url)

    db.session.commit()

    return jsonify(service.to_dict()), 200


@service_blueprint.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
	service = Service.query.get(service_id)

	if service is None:
		abort(404, description="Service not found")

	db.session.delete(service)
	db.session.commit()

	return jsonify(service.to_dict()), 200
