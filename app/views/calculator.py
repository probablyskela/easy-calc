from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from enum import Enum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt

calculator_blpr = Blueprint('calculator', __name__, url_prefix='/calculator')
calculators_blpr = Blueprint('calculators', __name__, url_prefix='/calculators')
bcrypt = Bcrypt()

@calculators_blpr.route('/', methods=['GET'])
def get_all_calculators():
	calculator_models = db.session.query(models.Calculator).all()

	res = []
	for calculator_model in calculator_models:
		calculator_json = {}

		calculator_json['id'] = calculator_model.id
		calculator_json['name'] = calculator_model.name
		calculator_json['description'] = calculator_model.description
		calculator_json['inputData'] = calculator_model.input_data
		calculator_json['code'] = calculator_model.code
		calculator_json['isPubic'] = calculator_model.is_public
		calculator_json['author_id'] = calculator_model.author_id

		res.append(calculator_json)
	
	return jsonify(res), 200

@calculator_blpr.route('/', methods=['POST'])
def create_new_calculator():
	class Calculator(Schema):
		name = fields.Str(required=True)
		description = fields.Str(required=True)
		inputData = fields.Str(required=True)
		code = fields.Str(required=True)
		isPublic = fields.Bool(required=True)
		authorId = fields.Int(required=True)
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Calculator().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	calculator = models.Calculator(
		name=request.json['name'],
		description=request.json['description'],
		input_data=request.json['inputData'],
		code=request.json['code'],
		is_public=request.json['isPublic'],
		author_id=request.json['authorId'])
	
	res = {}
	try:
		db.session.add(calculator)
		
	except:
		db.session.rollback()

	db.session.commit()
	
	res['id'] = calculator.id
	res['name'] = calculator.name
	res['description'] = calculator.description
	res['inputData'] = calculator.input_data
	res['code'] = calculator.code
	res['isPublic'] = calculator.is_public
	res['authorId'] = calculator.author_id

	return jsonify(res), 200

@calculator_blpr.route('/<int:calculator_id>', methods=['GET'])
def get_calculator(calculator_id):
	calculator = db.session.query(models.Calculator).filter_by(id=calculator_id).first()
	if calculator is None:
		return jsonify({'error': 'Calculator not found'}), 404

	res_model = db.session.query(
		models.Calculator, models.User 
	).filter(
		models.Calculator.id == calculator_id
	).join(
		models.User, models.User.id == models.Calculator.author_id
	).first()

	res = {}
	if res_model is None:
		return jsonify({'error': 'Calculator not found'}), 404
	
	calculator_model, user_model = res_model

	res['id'] = calculator_model.id
	res['name'] = calculator_model.name
	res['description'] = calculator_model.description
	res['inputData'] = calculator_model.input_data
	res['code'] = calculator_model.code
	res['isPublic'] = calculator_model.is_public
	
	res['author'] = {}
	res['author']['id'] = user_model.id
	res['author']['email'] = user_model.email
	res['author']['username'] = user_model.username
	res['author']['role'] = user_model.role

	res['author']['calculatorIds'] = [int(row.id) for row in db.session.query(models.Calculator).filter_by(author_id=user_model.id).all()]
	

	return jsonify(res), 200

@calculator_blpr.route('/<int:calculator_id>', methods=['PATCH'])
def update_calculator(calculator_id):

	class Calculator(Schema):
		name = fields.Str(required=False)
		description = fields.Str(required=False)
		inputData = fields.Str(required=False)
		code = fields.Str(required=False)
		isPublic = fields.Bool(required=False)
	
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Calculator().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	calculator_model = db.session.query(models.Calculator).filter_by(id=calculator_id).first()
	if calculator_model is None:
		return jsonify({'error': 'Calculator not found'}), 404

	try:
		if 'name' in request.json:
			calculator_model.name = request.json['name']
		if 'description' in request.json:
			calculator_model.description = request.json['description']
		if 'inputData' in request.json:
			calculator_model.input_data = request.json['inputData']
		if 'code' in request.json:
			calculator_model.code = request.json['code']
		if 'isPublic' in request.json:
			calculator_model.is_public = request.json['isPublic']
	except:
		db.session.rollback()
		return jsonify({'error': 'Database error'}), 500

	db.session.commit()

	return get_calculator(calculator_id)

@calculator_blpr.route('/<int:calculator_id>', methods=['DELETE'])
def delete_calculator(calculator_id):
	calculator_model = db.session.query(models.Calculator).filter_by(id=calculator_id).first()
	if calculator_model is None:
		return jsonify({'error': 'Calculator not found'}), 404

	try:
		db.session.delete(calculator_model)
	except:
		db.session.rollback()
		return jsonify({'error': 'Database error'}), 500

	db.session.commit()
	return {'message': 'Calculator deleted successfully'}, 200


@calculators_blpr.route('/<int:calculator_id>/reviews', methods=['GET'])
def get_all_reviws_for_calculator(calculator_id):	
	if db.session.query(models.Calculator).filter_by(id=calculator_id).first() is None:
		return jsonify({'error': 'Calculator not found'}), 404

	reviews = db.session.query(models.Review).filter(models.Review.calculator_id==calculator_id).all()
	res = []
	for review in reviews:
		current = {}

		current['id'] = review.id
		current['message'] = review.message
		current['rating'] = review.rating
		current['authorId'] = review.author_id
		
		res.append(current)

	return jsonify(res), 200

@calculators_blpr.route('/<int:review_calculator_id>/reviews', methods=['POST'])
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

	if not(0 <= request.json['rating'] <= 5):
		return jsonify({'error': 'Rating must be between 0 and 5'}), 400

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