from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from enum import Enum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt

reviews_blpr = Blueprint('review', __name__, url_prefix='/')

@reviews_blpr.route('/calculator/<int:calculator_id>/reviews', methods=['GET'])
def get_all_reviws_for_calculator(calculator_id):	
	if db.session.query(models.Calculator).filter_by(id=calculator_id).first() is None:
		return jsonify({'error': 'Calculator not found'}), 404

	reviews = db.session.query(models.Review).filter_by(calculatorId=calculator_id).all()
	res = []
	for review in reviews:
		current = {}

		current['id'] = review.id
		current['message'] = review.message
		current['rating'] = review.rating
		current['authorId'] = review.authorId
		
		res.append(current)

	return jsonify(res), 200

@reviews_blpr.route('/calculator/<int:review_calculator_id>/review', methods=['POST'])
def add_review_to_calculator(review_calculator_id):
	if db.session.query(models.Calculator).filter_by(id=review_calculator_id).first() is None:
		return jsonify({'error': 'Calculator not found'}), 404

	class Review(Schema):
		message = fields.Str(required=True)
		rating = fields.Int(required=True)
		authorId = fields.Int(required=True)

	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Review().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	old_review = db.session.query(
		models.Review 
	).filter(
		models.Review.calculator_id == review_calculator_id, models.Review.author_id == request.json['authorId']
	).first()
	
	if old_review is not None:
		return jsonify({'error': 'Review already exists'}), 400

	review = models.Review(message = request.json['message'], rating = request.json['rating'], author_id = request.json['authorId'], calculator_id=review_calculator_id)

	try:
		db.session.add(review)
	except:
		return jsonify({'error': 'Failed to add review'}), 500

	db.session.commit()

	res = request.json
	res['id'] = review.id

	return jsonify(res), 200

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

