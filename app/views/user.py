from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField
from enum import Enum, IntEnum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from app import app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

jwt = JWTManager(app)
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
		user = User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	new_user_model = models.User(email = user['email'], username = user['username'], password = bcrypt.generate_password_hash(user['password']).decode('utf-8'), role = user['role'])
	user_already_exists = db.session.query(models.User).filter(models.User.username == new_user_model.username or models.User.email == new_user_model.email).count() != 0
	if user_already_exists:
		return jsonify({'error': 'User already exists'}), 400

	db.session.add(new_user_model)


	db.session.commit()

	return get_user(new_user_model.id)


@user_blueprint.route('/login', methods=['POST'])
def login():
	class Login(Schema):
		username = fields.Str(required=True)
		password = fields.Str(required=True)

	try:
		if not request.json:
			raise ValidationError('No input data provided')
		login = Login().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	user = db.session.query(models.User).filter(models.User.username == login['username']).first()
	if not user:
		return jsonify({'error': 'User does not exist'}), 400

	if not bcrypt.check_password_hash(user.password, login['password']):
		return jsonify({'error': 'Wrong password'}), 400

	access_token = create_access_token(identity=user.id)
	return jsonify({"token": access_token}), 200


@user_blueprint.route('/logout', methods=['GET'])
@jwt_required()
def logout():
	return jsonify({"message": "Successfully logged out"}), 200


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
@jwt_required()
def update_user(user_id):	
	try:
		class User(Schema):
			email = fields.Email(required=False)
			username = fields.Str(required=False)
			password = fields.Str(required=False)
			role = EnumField(UserRole, by_value=False, required=False)

		if not request.json:
			raise ValidationError('No input data provided')
		user = User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	new_user = db.session.query(models.User).filter(models.User.id == user_id).first()
	if new_user is None:
		return jsonify({'error': 'User does not exist'}), 404
	
	if new_user.id != get_jwt_identity() and new_user.role != UserRole.Administrator:
		return jsonify({'error': 'Access denied'}), 403
	
	if 'email' in user:
		new_user.email = user['email']
	if 'username' in user:
		new_user.username = user['username']
	if 'password' in user:
		new_user.password = bcrypt.generate_password_hash(user['password']).decode('utf-8')
	if 'role' in user:
		new_user.role = user['role']


	db.session.commit()

	return get_user(user_id)

@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
	user = db.session.query(models.User).filter(models.User.id == user_id).first()
	if user is None:
		return jsonify({'error': 'User does not exist'}), 404

	if user.id != get_jwt_identity() and user.role != UserRole.Administrator:
		return jsonify({'error': 'Access denied'}), 403
	
	db.session.delete(user)	

	
	db.session.commit()

	return "", 204
