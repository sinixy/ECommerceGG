from flask_restful import Resource, marshal
from ..models import Product, Category, Game, CategoryGame
from ..common.inputs import product_parser
from ..common.outputs import product_fields


class ProductResource(Resource):
	def get(self, product_id=None):
		if product_id:
			product = Product.query.get(product_id)
			if product:
				return marshal(product, product_fields), 200
			else:
				return {'data': {}, 'errors': ['No such product'], 'msg': 'error'}, 404
		else:
			args = product_parser.parse_args(strict=True)
			query = Product.query

			category_game_filters = {}
			if args['category']:
				category = Category.query.filter_by(name=args['category']).first()
				if not category:
					return {'data': [], 'errors': ['No such category'], 'msg': 'error'}, 404
				category_game_filters['category_id'] = category.id
			if args['game']:
				game = Game.query.filter_by(name=args['game']).first()
				if not game:
					return {'data': [], 'errors': ['No such game'], 'msg': 'error'}, 404
				category_game_filters['game_id'] = game.id

			if category_game_filters:
				category_game_list = CategoryGame.query.filter_by(**category_game_filters).all()
				query = query.filter(Product.category_game_id.in_([cg.id for cg in category_game_list]))

			if args['q']:
				query = query.filter(Product.title.ilike(f'%{args["q"]}%'))

			if args['minPrice']:
				query = query.filter(args['minPrice'] <= Product.price)
			if args['maxPrice']:
				query = query.filter(Product.price < args['maxPrice'])

			return {'data': marshal(query.all(), product_fields), 'errors': [], 'msg': 'ok'}, 200