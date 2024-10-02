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
@jwt_required()  # Este decorador asegura que solo los usuarios autenticados pueden acceder a este endpoint
def create_service():
    data = request.json

    name = data.get('name')
    description = data.get('description')
    aprox_price = data.get('aprox_price')
    fee = data.get('fee')
    category = data.get('category')
    img_url = data.get('img_url')  # Este debe ser el base64

    if not img_url:
        return jsonify({"error": "No image URL or file provided"}), 400

    # Si img_url es una URL, conviértelo a base64
    if img_url.startswith('http'):
        img_data = convert_image_to_base64(img_url)
    else:
        img_data = img_url  # Suponiendo que ya es base64

    service = Service(
        name=name,
        description=description,
        aprox_price=aprox_price,
        fee=fee,
        category=category,
        img_data=img_data
    )
    service = Service(name="Servicio 1", img_url=encode_image("ruta_a_la_imagen.jpg"))
    db.session.add(service)
    db.session.commit()

    return jsonify({"message": "Service created successfully"}), 201

def convert_image_to_base64(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    buffered = BytesIO()
    img.save(buffered, format="PNG")  # Cambia el formato si es necesario
    img_str = base64.b64encode(buffered.getvalue()).decode()  # Convertir a base64

    # Imprimir para verificar el formato
    print(f"Base64 Image Data: {img_str[:50]}...")  # Imprime los primeros 50 caracteres para verificar

    return f"data:image/png;base64,{img_str}"






@service_blueprint.route('/api/services', methods=['GET'])
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
