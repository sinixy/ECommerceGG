from flask_restful import Resource, marshal
from models import Country
from common.outputs import country_fields


class CountryResource(Resource):
	def get(self):
		return {'data': {'countries': marshal(Country.query.all(), country_fields)}, 'status': 'success'}