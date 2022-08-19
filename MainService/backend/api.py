from flask import Blueprint
from flask_restful import Api
from .resources import CategoryResource, GameResource, ProductResource, ReviewResource, CartResource, UserResource


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(CategoryResource, '/category', '/category/<int:category_id>')
api.add_resource(GameResource, '/game', '/game/<int:game_id>')
api.add_resource(ProductResource, '/product', '/product/<int:product_id>')
api.add_resource(ReviewResource, '/review', '/review/<int:review_id>')
api.add_resource(CartResource, '/cart')
api.add_resource(UserResource, '/user', '/user/<int:user_id>')