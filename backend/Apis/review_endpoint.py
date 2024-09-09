from flask import request, jsonify, abort, Blueprint
from models.review import Review
from Data.DataManager import DataManager
from database import db

review_blueprint = Blueprint('review_blueprint', __name__)
data_manager = DataManager()


@review_blueprint.route('/reviews', methods=['POST'])
def create_review():
    if not request.json or not 'service_id' in request.json or not 'user_id' in request.json or not 'rating' in request.json:
        abort(400, description="Missing required fields")

    service_id = request.json['service_id']
    user_id = request.json['user_id']
    rating = request.json['rating']

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        abort(400, description="Invalid rating value")

    review = Review(
        service_id=service_id,
        user_id=user_id,
        comment=request.json.get('comment', ''),
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
