from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.database import db
from backend.models.docs import Docs  # Asegúrate de que la importación sea correcta

docs_blueprint = Blueprint('docs_blueprint', __name__)

@docs_blueprint.route('/docs', methods=['POST'])
@jwt_required()
def create_document():
    claims = get_jwt()
    if not claims.get('is_admin'):
        abort(403, description='Admin rights required')

    if not request.json or 'user_id' not in request.json or 'title' not in request.json or 'content' not in request.json or 'file_id' not in request.json or 'doc_type' not in request.json or 'status' not in request.json:
        abort(400, description='Missing required fields')

    user_id = request.json.get('user_id')  # Cambia esto para usar get
    title = request.json.get('title')
    content = request.json.get('content')
    file_id = request.json.get('file_id')
    doc_type = request.json.get('doc_type')
    status = request.json.get('status')

    docs = Docs(
        user_id=user_id,
        title=title,
        content=content,
        file_id=file_id,
        doc_type=doc_type,
        status=status
    )

    db.session.add(docs)
    db.session.commit()

    return jsonify({"msg": "Document was created successfully", "docs_id": docs.id}), 201
