from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.Data.DataManager import DataManager
from backend.database import db
from backend.models.review import Review
from backend.models.service import Service

review_blueprint = Blueprint('review_blueprint', __name__)
data_manager = DataManager()


@review_blueprint.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()

    # Verifica si la solicitud tiene JSON
    if not request.is_json:
        abort(400, description="Request body must be JSON")

    # Desglosa y verifica los parámetros
    data = request.get_json()

    service_id = data.get('service_id')
    comment = data.get('comment')
    rating = data.get('rating')

    if not service_id or not comment or rating is None:
        abort(422, description="Missing parameters or invalid values")

    if len(comment) > 1024:
        abort(400, description="Comment is too long")

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        abort(400, description="Invalid rating value")

    # Busca el servicio
    service = Service.query.get(service_id)
    if not service:
        abort(404, description="Service not found")

    # Crea la reseña
    review = Review(
        service_id=service_id,
        user_id=current_user_id,
        comment=comment,
        rating=rating
    )
    db.session.add(review)
    db.session.commit()

    return jsonify(review.to_dict()), 201






@review_blueprint.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200


@review_blueprint.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
	review = Review.query.get(review_id)
	if review is None:
		abort(404, description="Review not found")
	return jsonify(review.to_dict()), 200


@review_blueprint.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if review is None:
        abort(404, description="Review not found")

    data = request.get_json()
    review.comment = data.get('comment', review.comment)
    review.rating = data.get('rating', review.rating)
    review.service_id = data.get('service_id', review.service_id)
    review.user_id = data.get('user_id', review.user_id)

    db.session.commit()
    return jsonify(review.to_dict()), 200


@review_blueprint.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
	review = Review.query.get(review_id)
	if not review:
		abort(404, description="Review not found")

	db.session.delete(review)
	db.session.commit()
	return '', 204
