from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db

reviews_blpr = Blueprint('review', __name__, url_prefix='/review')

@reviews_blpr.route('/review/<int:review_id>', methods=['PATCH'])
def update_review(review_id):
	review = db.session.query(models.Review).filter_by(id=review_id).first()
	if review is None:
		return jsonify({'error': 'Review not found'}), 404

	class Review(Schema):
		message = fields.Str(required=False)
		rating = fields.Int(required=False)
	
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Review().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	try:
		if 'message' in request.json:
			review.message = request.json['message']
		if 'rating' in request.json:
			if not(0 <= request.json['rating'] <= 5):
				return jsonify({'error': 'Rating must be between 0 and 5'}), 400
			review.rating = request.json['rating']
	except:
		db.session.rollback()
		return jsonify({'error': 'Failed to update review'}), 500

	db.session.commit()

	res = {}
	res['id'] = review.id
	res['message'] = review.message
	res['rating'] = review.rating

	return jsonify(res), 200

@reviews_blpr.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
	review = db.session.query(models.Review).filter_by(id=review_id).first()
	if review is None:
		return jsonify({'error': 'Review not found'}), 404
	
	try:
		db.session.delete(review)
	except:
		db.session.rollback()
		return jsonify({'error': 'Failed to delete review'}), 500

	db.session.commit()
	return jsonify({'message': 'Review deleted'}), 204

