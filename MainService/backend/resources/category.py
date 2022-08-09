from flask_restful import Resource, marshal
from ..models import Category
from ..common.outputs import category_fields


class CategoryResource(Resource):
	def get(self, category_id=None):
		if category_id:
			category = Category.query.get(category_id)
			if category:
				return marshal(category, category_fields), 200
			else:
				return {'data': {}, 'errors': ['No such category'], 'msg': 'error'}, 404
		else:
			return marshal(Category.query.all(), category_fields), 200