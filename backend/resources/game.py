from flask_restful import Resource, marshal
from models import Game, CategoryGame
from common.inputs import game_parser
from common.outputs import game_fields


class GameResource(Resource):
	def get(self, game_id=0):
		if game_id:
			game = Game.query.get(game_id)
			if game:
				return {'data': {'game': marshal(game, game_fields)}, 'status': 'success'}
			else:
				return {'status': 'error', 'message': 'No such game'}, 404
		else:
			query = Game.query
			args = game_parser.parse_args()
			if category_id := args['categoryId']:
				category_game_list = CategoryGame.query.filter_by(category_id=category_id).all()
				query = query.filter(Game.id.in_([cg.game_id for cg in category_game_list]))
			return {'data': {'games': marshal(query.all(), game_fields)}, 'status': 'success'}