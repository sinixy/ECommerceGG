from flask_restful import Resource, marshal
from ..models import Category
from ..common.outputs import category_fields


class CategoryResource(Resource):
	def get(self, category_id=0):
		if category_id:
			category = Category.query.get(category_id)
			if category:
				return {'data': {'category': marshal(category, category_fields)}, 'status': 'success'}
			else:
				return {'status': 'error', 'message': 'No such category'}, 404
		else:
			return {'data': {'categories': marshal(Category.query.all(), category_fields)}, 'status': 'success'}