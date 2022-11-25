from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from app.views.user import UserRole
from app import app
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity
)

jwt = JWTManager(app)
reviews_blpr = Blueprint('review', __name__, url_prefix='/review')

@reviews_blpr.route('/<int:review_id>', methods=['PATCH'])
@jwt_required()
def update_review(review_id):
	new_review = db.session.query(models.Review).filter_by(id=review_id).first()
	if new_review is None:
		return jsonify({'error': 'Review not found'}), 404
	
	user = db.session.query(models.User).filter_by(id=get_jwt_identity()).first()
	if new_review.author_id != get_jwt_identity() and user.role != UserRole.Administrator and user.role != UserRole.Moderator:
		return jsonify({'error': 'Access denied'}), 403

	class Review(Schema):
		message = fields.Str(required=False)
		rating = fields.Int(required=False)
	
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		review = Review().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	if 'message' in review:
		new_review.message = review['message']
	if 'rating' in review:
		if not(0 <= review['rating'] <= 5):
			return jsonify({'error': 'Rating must be between 0 and 5'}), 400
		new_review.rating = review['rating']


	db.session.commit()

	res = {}
	res['id'] = new_review.id
	res['message'] = new_review.message
	res['rating'] = new_review.rating

	return jsonify(res), 200

@reviews_blpr.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
	review = db.session.query(models.Review).filter_by(id=review_id).first()
	if review is None:
		return jsonify({'error': 'Review not found'}), 404

	user = db.session.query(models.User).filter_by(id=get_jwt_identity()).first()
	if review.author_id != get_jwt_identity() and user.role != UserRole.Administrator and user.role != UserRole.Moderator:
		return jsonify({'error': 'Access denied'}), 403

	db.session.delete(review)


	db.session.commit()
	return jsonify({'message': 'Review deleted'}), 204

