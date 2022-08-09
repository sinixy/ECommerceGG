from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from .common.inputs import token_create_parser
from .models import User


auth_blueprint = Blueprint('auth', __name__)
auth = Api(auth_blueprint)


def login_required(f):
	def decorator(*args, **kwargs):
		verify_jwt_in_request()
		current_user = User.query.get(get_jwt_identity())
		if current_user:
			return f(current_user, *args, **kwargs)
		else:
			return {'data': {}, 'errors': ['No such user'], 'msg': 'error'}, 404
	return decorator

def login(user_id):
	response = jsonify({'msg': 'ok'})
	set_access_cookies(response, create_access_token(identity=user_id))
	return response

def logout():
	response = jsonify({'msg': 'ok'})
	unset_jwt_cookies(response)
	return response

class TokenResource(Resource):

	def get(self):
		verify_jwt_in_request()
		return {'userId': get_jwt_identity(), 'msg': 'ok'}

	def post(self):
		args = token_create_parser.parse_args(strict=True)

		user = User.query.filter_by(username=args['username']).first()
		if not user:
			return {'data': {}, 'errors': ['No such user'], 'msg': 'error'}, 404

		if not user.verify_password(args['password']):
			return {'data': {}, 'errors': ['Invalid password'], 'msg': 'error'}, 401

		return login(user.id)

	def delete(self):
		return logout()


auth.add_resource(TokenResource, '/token')


