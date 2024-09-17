from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database import db
from models.address import Address
from models.user import User


address_blueprint = Blueprint('address_blueprint', __name__)

@address_blueprint.route('/users/<user_id>/addresses', methods=['POST'])
@jwt_required()
def create_address(user_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    # Verificar si el usuario es el mismo o es admin
    if current_user_id != user_id and not claims.get('is_admin', False):
        abort(403, description="Not authorized to create address for this user")

    # Verificar que todos los campos requeridos están en la solicitud
    if not request.json or not all(k in request.json for k in ('street', 'city', 'state', 'zip_code')):
        abort(400, description="Missing required fields")

    # Obtener el usuario de la base de datos
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

    # Guardar la dirección en la base de datos
    db.session.add(address)
    db.session.commit()

    return jsonify(address.to_dict()), 201




@address_blueprint.route('/addresses/<address_id>', methods=['GET'])
@jwt_required()
def get_address(address_id):
    current_user_id = get_jwt_identity()
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    if address.user_id != current_user_id:
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, description="Not authorized to view this address")

    return jsonify(address.to_dict())





@address_blueprint.route('/addresses/<address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    current_user_id = get_jwt_identity()
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    if address.user_id!= current_user_id:
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, description="Not authorized to update this address")

    data = request.json

    address.street = data.get('street', address.street)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zip_code = data.get('zip_code', address.zip_code)

    db.session.commit()

    return jsonify(address.to_dict())





@address_blueprint.route('/addresses/<address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    current_user_id = get_jwt_identity()
    address = Address.query.get(address_id)
    if not address:
        abort(404, description="Address not found")

    if address.user_id!= current_user_id:
        claims = get_jwt()
        if not claims.get('is_admin'):
            abort(403, description="Not authorized to delete this address")

    db.session.delete(address)
    db.session.commit()

    return jsonify({"message": "Address deleted"}), 200
