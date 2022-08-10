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
		try:
			jwt = verify_jwt_in_request(optional=True)
		except Exception as e:
			return {'status': 'error', 'message': f'Invalid JWT. {str(e)}'}, 401
		if not jwt:
			return {'status': 'error', 'message': 'Login required'}, 401

		jwt_header, jwt_data = jwt
		current_user = User.query.get(jwt_data['sub'])
		if current_user:
			return f(current_user, *args, **kwargs)
		else:
			return {'status': 'error', 'message': 'No such user'}, 404
	return decorator

def login(user_id):
	response = jsonify({'data': None, 'status': 'success'})
	set_access_cookies(response, create_access_token(identity=user_id))
	return response

def logout():
	response = jsonify({'data': None, 'status': 'success'})
	unset_jwt_cookies(response)
	return response

class TokenResource(Resource):
	method_decorators = {'get': [login_required]}

	def get(self):
		return {'status': 'success', 'data': {'userId': get_jwt_identity()}}

	def post(self):
		args = token_create_parser.parse_args()

		user = User.query.filter_by(username=args['username']).first()
		if not user:
			return {'status': 'error', 'message': 'No such user'}, 404

		if not user.verify_password(args['password']):
			return {'status': 'error', 'message': 'Invalid password'}, 401

		return login(user.id)

	def delete(self):
		return logout()


auth.add_resource(TokenResource, '/token')


