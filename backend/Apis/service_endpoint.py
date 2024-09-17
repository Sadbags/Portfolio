from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.service import Service
from database import db


service_blueprint = Blueprint('service_blueprint', __name__)


@service_blueprint.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    current_user_id = get_jwt_identity()  # Obtenemos el user_id del token JWT

    if not request.json or not 'name' in request.json or not 'aprox_price' in request.json or not 'category' in request.json:
        abort(400, description="Missing parameters")

    # Recogemos los datos del JSON
    name = request.json['name']
    description = request.json.get('description', '')  # Opcional
    aprox_price = request.json['aprox_price']
    category = request.json['category']
    fee = request.json['fee']
    img_url = request.json.get('img_url', '')  # Opcional

    # Crear el servicio
    new_service = Service(
        name=name,
        description=description,
        aprox_price=aprox_price,
        category=category,
        fee=fee,
        img_url=img_url,
        user_id=current_user_id  # Relacionamos el servicio con el usuario autenticado
    )
    db.session.add(new_service)
    db.session.commit()

    return jsonify(new_service.to_dict()), 201




@service_blueprint.route('/services', methods=['GET'])
def get_services():
	services = Service.query.all()

	return jsonify([service.to_dict() for service in services]), 200


@service_blueprint.route('/services/<service_id>', methods=['GET'])
def get_service(service_id):
	service = Service.query.get(service_id)

	if service is None:
		abort(404, description="Service not found")

	return jsonify(service.to_dict()), 200


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
