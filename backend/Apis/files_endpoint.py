from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.database import db
from backend.models.files import Files
from backend.models.docs import Docs

files_blueprint = Blueprint('files_blueprint', __name__)

@files_blueprint.route('/files', methods=['POST'])
@jwt_required()
def upload_file():
    # Obtener el usuario actual
    user_id = get_jwt_identity()

    # Validar los datos de entrada
    if not request.json or 'docs_id' not in request.json or 'filename' not in request.json or 'file_url' not in request.json or 'file_size' not in request.json or 'file_type' not in request.json:
        abort(400, description='Missing required fields')

    docs_id = request.json['docs_id']
    filename = request.json['filename']
    file_url = request.json['file_url']
    file_size = request.json['file_size']
    file_type = request.json['file_type']

    # Verificar que el documento exista
    document = Docs.query.get(docs_id)
    if document is None:
        abort(404, description='Document not found')

    # Crear una instancia de Files
    new_file = Files(
        user_id=user_id,
        filename=filename,
        file_url=file_url,
        file_size=file_size,
        file_type=file_type,
        docs_id=docs_id
    )

    # Agregar el archivo a la sesión de la base de datos y hacer commit
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"msg": "File uploaded successfully", "file_id": new_file.id}), 201
