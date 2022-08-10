from flask_restful import Resource, marshal
from ..models import Game
from ..common.outputs import game_fields


class GameResource(Resource):
	def get(self, game_id=0):
		if game_id:
			game = Game.query.get(game_id)
			if game:
				return {'data': {'game': marshal(game, game_fields)}, 'status': 'success'}
			else:
				return {'status': 'error', 'message': 'No such game'}, 404
		else:
			return {'data': {'games': marshal(Game.query.all(), game_fields)}, 'status': 'success'}