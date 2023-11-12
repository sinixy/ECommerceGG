from flask_restful import Resource, marshal
from email_validator import validate_email, EmailNotValidError
from models import db, User, Country, Cart
from auth import login_required, login, logout
from common.inputs import user_create_parser, user_edit_parser
from common.outputs import user_fields


def access_required(f):
	def decorator(current_user, user_id=0):
		user = User.query.get(user_id)
		if not user:
			return {'status': 'error', 'message': 'No such user'}, 404
		if user.id != current_user.id:
			return {'status': 'error', 'message': 'Access denied'}, 403
		return f(current_user)
	return decorator

class UserResource(Resource):
	method_decorators = {
		'patch': [access_required, login_required],
		'delete': [access_required, login_required]
	}

	def get(self, user_id=0):
		user = User.query.get(user_id)
		if user:
			return {'data': {'user': marshal(user, user_fields)}, 'status': 'success'}
		else:
			return {'status': 'error', 'message': 'No such user'}, 404

	def post(self, user_id=0):
		if user_id:
			return {'data': {}, 'errors': ['Invalid endpoint'], 'msg': 'error'}, 400

		args = user_create_parser.parse_args(strict=True)
		username = args['username']
		password = args['password']
		email = args['email']
		country_id = args['countryId']
		country = Country.query.get(country_id)
		if not country:
			return {'status': 'error', 'message': 'No such country'}, 404

		try:
			email_validation = validate_email(email)
			email = email_validation.email
		except EmailNotValidError:
			return {'data': {'email': 'Invalid email'}, 'status': 'fail'}, 400

		if User.query.filter_by(email=email).first():
			return {'data': {'email': 'This email is already taken'}, 'status': 'fail'}, 400
		if User.query.filter_by(username=username).first():
			return {'data': {'username': 'This username is already taken'}, 'status': 'fail'}, 400

		if len(username) < 4:
			return {'data': {'username': 'Username is too short'}, 'status': 'fail'}, 400
		if len(password) < 8:
			return {'data': {'password': 'Password is too short'}, 'status': 'fail'}, 400

		new_user = User(username=username, email=email, country_id=country_id, role_id=1)
		new_user.set_password(password)
		db.session.add(new_user)
		db.session.commit()

		new_cart = Cart(user_id=new_user.id)
		db.session.add(new_cart)
		db.session.commit()

		return login(new_user)

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
				return {'status': 'error', 'message': 'No such country'}, 404

		if username != current_user.username:
			if len(username) < 4:
				return {'data': {'username': 'Username is too short'}, 'status': 'fail'}, 400
			if User.query.filter_by(username=username).first():
				return {'data': {'username': 'This username is already taken'}, 'status': 'fail'}, 400

		if email != current_user.email:
			try:
				email_validation = validate_email(email)
				email = email_validation.email
			except EmailNotValidError:
				return {'data': {'email': 'Invalid email'}, 'status': 'fail'}, 400
			if User.query.filter_by(email=email).first():
				return {'data': {'email': 'This email is already taken'}, 'status': 'fail'}, 400

		if not current_user.verify_password(old_password):
			return {'data': {'oldPassword': 'Got incorrect current password'}, 'status': 'fail'}, 400
		if len(new_password) < 8:
			return {'data': {'newPassword': 'New password is too short'}, 'status': 'fail'}, 400

		current_user.username = username
		current_user.email = email
		current_user.country_id = country_id
		current_user.set_password(new_password)
		db.session.commit()

		return {'data': {'user': marshal(current_user, user_fields)}, 'status': 'success'}
			
	def delete(self, current_user):
		db.session.delete(current_user)
		db.session.commit()

		return logout()
