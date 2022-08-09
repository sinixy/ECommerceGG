from flask_restful import Resource, marshal
from ..models import Game
from ..common.outputs import game_fields


class GameResource(Resource):
	def get(self, game_id=None):
		if game_id:
			game = Game.query.get(game_id)
			if game:
				return marshal(game, game_fields), 200
			else:
				return {'data': {}, 'errors': ['No such game'], 'status': 'error'}, 404
		else:
			return marshal(Game.query.all(), game_fields), 200