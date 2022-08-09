from flask_restful import Resource, marshal
from email_validator import validate_email, EmailNotValidError
from ..models import db, User, Country
from ..auth import login_required, login, logout
from ..common.inputs import user_create_parser, user_edit_parser
from ..common.outputs import user_fields


def access_required(f):
	def decorator(current_user, user_id=None):
		user = User.query.get(user_id)
		if not user:
			return {'data': {}, 'errors': ['No such user'], 'msg': 'error'}, 404
		if user.id != current_user.id:
			return {'data': {}, 'errors': ['Access denied'], 'msg': 'error'}, 403
		return f(current_user)
	return decorator

class UserResource(Resource):
	method_decorators = {
		'patch': [access_required, login_required],
		'delete': [access_required, login_required]
	}

	def get(self, user_id=None):
		if user_id:
			user = User.query.get(user_id)
			if user:
				return marshal(user, user_fields), 200
			else:
				return {'data': {}, 'errors': ['No such user'], 'msg': 'error'}, 404
		else:
			return {'data': {}, 'errors': ['Invalid endpoint'], 'msg': 'error'}, 200

	def post(self, user_id=None):
		if user_id:
			return {'data': {}, 'errors': ['Invalid endpoint'], 'msg': 'error'}, 400

		args = user_create_parser.parse_args(strict=True)
		username = args['username']
		password = args['password']
		email = args['email']
		country_id = args['countryId']
		country = Country.query.get(country_id)
		if not country:
			return {'data': {}, 'errors': ['No such country'], 'msg': 'error'}

		try:
			email_validation = validate_email(email)
			email = email_validation.email
		except EmailNotValidError:
			return {'data': {}, 'errors': ['Invalid email'], 'msg': 'error'}

		if User.query.filter_by(email=email).first():
			return {'data': {}, 'errors': ['This email is already taken'], 'msg': 'error'}
		if User.query.filter_by(username=username).first():
			return {'data': {}, 'errors': ['This username is already taken'], 'msg': 'error'}

		if len(username) < 4:
			return {'data': {}, 'errors': ['Username is too short'], 'msg': 'error'}
		if len(password) < 8:
			return {'data': {}, 'errors': ['Password is too short'], 'msg': 'error'}

		new_user = User(username=username, email=email, country_id=country_id, role_id=1)
		new_user.set_password(password)
		db.session.add(new_user)
		db.session.commit()
		db.session.refresh(new_user)

		return login(new_user.id)

	def patch(self, current_user):
		args = user_edit_parser.parse_args(strict=True)
		username = args['username']
		old_password = args['oldPassword']
		new_password = args['newPassword']
		email = args['email']
		country_id = args['countryId']

		if country_id != current_user.country_id:
			country = Country.query.get(country_id)
			if not country:
				return {'data': {}, 'errors': ['No such country'], 'msg': 'error'}

		if username != current_user.username:
			if len(username) < 4:
				return {'data': {}, 'errors': ['Username is too short'], 'msg': 'error'}
			if User.query.filter_by(username=username).first():
				return {'data': {}, 'errors': ['This username is already taken'], 'msg': 'error'}

		if email != current_user.email:
			try:
				email_validation = validate_email(email)
				email = email_validation.email
			except EmailNotValidError:
				return {'data': {}, 'errors': ['Invalid email'], 'msg': 'error'}
			if User.query.filter_by(email=email).first():
				return {'data': {}, 'errors': ['This email is already taken'], 'msg': 'error'}

		if not current_user.verify_password(old_password):
			return {'data': {}, 'errors': ['Wrong password']}, 401
		if len(new_password) < 8:
			return {'data': {}, 'errors': ['Password is too short'], 'msg': 'error'}

		current_user.username = username
		current_user.email = email
		current_user.country_id = country_id
		current_user.set_password(new_password)
		db.session.commit()

		return {'data': {}, 'errors': [], 'msg': 'ok'}, 204
			
	def delete(self, current_user):
		db.session.delete(current_user)
		db.session.commit()

		return logout()
