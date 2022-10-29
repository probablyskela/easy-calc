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

def from_calculator_model_to_json(calculator: models.Calculator):
	calculator_json = {}

	calculator_json['id'] = calculator.id
	calculator_json['name'] = calculator.name
	calculator_json['description'] = calculator.description
	calculator_json['inputData'] = calculator.inputData
	calculator_json['code'] = calculator.code
	calculator_json['isPubic'] = calculator.isPublic
	calculator_json['ownerId'] = calculator.ownerId

	return jsonify(calculator_json)

@calculators_blpr.route('/', methods=['GET'])
def get_all_calculators():
	calculator_models = db.session.query(models.Calculator).all()
	all_calculator_jsons = [from_calculator_model_to_json(calculator_model) for calculator_model in calculator_models]

	return jsonify(all_calculator_jsons), 200

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

	return {'message': 'Calculator created successfully'}, 201

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

