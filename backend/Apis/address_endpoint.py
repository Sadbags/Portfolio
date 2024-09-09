from flask import request, jsonify, abort, Blueprint
from backend.database import db
from backend.models.address import Address
from backend.models.user import User


address_blueprint = Blueprint('address_blueprint', __name__)

@address_blueprint.route('/users/<user_id>/addresses', methods=['POST'])
def create_address(user_id):
    # Verificar que todos los campos requeridos están en la solicitud
    if not request.json or not all(k in request.json for k in ('street', 'city', 'state', 'zip_code')):
        abort(400, description="Missing required fields")

    # Obtener los datos del usuario
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    # Crear la nueva dirección
    address = Address(
        street=request.json['street'],
        city=request.json['city'],
        state=request.json['state'],
        zip_code=request.json['zip_code'],
        user_id=user_id
    )

    # Agregar la dirección a la base de datos
    db.session.add(address)
    db.session.commit()

    return jsonify(address.to_dict()), 201


@address_blueprint.route('/addresses/<address_id>', methods=['GET'])
def get_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    return jsonify(address.to_dict())


@address_blueprint.route('/addresses/<address_id>', methods=['PUT'])
def update_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    data = request.json

    address.street = data.get('street', address.street)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zip_code = data.get('zip_code', address.zip_code)

    db.session.commit()

    return jsonify(address.to_dict())


@address_blueprint.route('/addresses/<address_id>', methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    db.session.delete(address)
    db.session.commit()

    return '', 204
