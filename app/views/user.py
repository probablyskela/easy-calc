from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from enum import Enum, IntEnum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
bcrypt = Bcrypt()

class UserRole(IntEnum):
	User = 1 
	Moderator = 2
	Administrator = 3

@user_blueprint.route('/', methods=['POST'])
def create_user():
	class User(Schema):
		email = fields.Email(required=True)
		username = fields.Str(required=True)
		password = fields.Str(required=True)
		role = EnumField(UserRole, by_value=False, required=True)

	try:
		if not request.json:
			raise ValidationError('No input data provided')
		User().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	new_user_model = models.User(email = request.json['email'], username = request.json['username'], password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'), role = request.json['role'])
	user_already_exists = db.session.query(models.User).filter(models.User.username == new_user_model.username or models.User.email == new_user_model.email).count() != 0
	if user_already_exists:
		return jsonify({'error': 'User already exists'}), 400

	try:
		db.session.add(new_user_model)
	except:
		db.session.rollback()
		return jsonify({"User data is not valid"}), 400

	db.session.commit()

	return get_user(new_user_model.id)

@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = db.session.query(models.User).filter_by(id=user_id).first()
	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	res_json = {}
	res_json['id'] = user.id
	res_json['email'] = user.email
	res_json['username'] = user.username
	res_json['role'] = user.role
	res_json['calculatorIds'] = [int(row.id) for row in db.session.query(models.Calculator).filter_by(author_id=user_id).all()]

	return jsonify(res_json), 200

@user_blueprint.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):	
	try:
		class User(Schema):
			email = fields.Email(required=False)
			username = fields.Str(required=False)
			password = fields.Str(required=False)
			role = EnumField(UserRole, by_value=False, required=False)

		if not request.json:
			raise ValidationError('No input data provided')
		User().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	user = db.session.query(models.User).filter(models.User.id == user_id).first()
	if user is None:
		return jsonify({'error': 'User does not exist'}), 404
	
	try:
		if 'email' in request.json:
			user.email = request.json['email']
		if 'username' in request.json:
			user.username = request.json['username']
		if 'password' in request.json:
			user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
		if 'role' in request.json:
			user.role = request.json['role']
	except:
		db.session.rollback()
		return jsonify({"User data is not valid"}), 400

	db.session.commit()

	return get_user(user_id)

@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	user = db.session.query(models.User).filter(models.User.id == user_id).first()
	if user is None:
		return jsonify({'error': 'User does not exist'}), 404
	
	try:
		db.session.delete(user)	
	except:
		db.session.rollback()
		return jsonify({"User data is not valid"}), 400
	
	db.session.commit()

	return "", 204

