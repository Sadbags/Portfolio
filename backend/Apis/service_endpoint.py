from flask import request, jsonify, abort, Blueprint
from backend.models.service import Service
from backend.database import db


service_blueprint = Blueprint('service_blueprint', __name__)


@service_blueprint.route('/services', methods=['POST'])
def create_service():
    def create_service():
        if not request.json:
            abort(400, description="Request body must be JSON")

    # Extract fields from JSON data
    name = request.json.get('name')
    description = request.json.get('description')
    aprox_price = request.json.get('aprox_price')
    category = request.json.get('category')
    fee = request.json.get('fee')
    img_url = request.json.get('img_url')

    # Validate required fields
    if not name or not aprox_price or not category or not fee:
        abort(400, description="Missing required fields")

    # Create a new Service instance
    service = Service(
        name=name,
        description=description,
        aprox_price=aprox_price,
        category=category,
        fee=fee,
        img_url=img_url
    )

    # Add the service to the database
    db.session.add(service)
    db.session.commit()

    # Return the created service as JSON
    return jsonify(service.to_dict()), 201



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
