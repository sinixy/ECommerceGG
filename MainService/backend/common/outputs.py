from flask_restful import fields


image_fields = {
	'id': fields.Integer,
	'url': fields.String
}

gallery_fields = {
	'id': fields.Integer,
	'type': fields.String,
	'images': fields.List(fields.Nested(image_fields, allow_null=True))
}

category_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'icon': fields.Nested(image_fields, allow_null=True)
}

game_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'icon': fields.Nested(image_fields, allow_null=True)
}

category_game_fields = {
	'id': fields.Integer,
	'category_id': fields.Integer,
	'game_id': fields.Integer
}

product_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'description': fields.String,
	'price': fields.Float,
	'available_quantity': fields.Integer,
	'min_quantity': fields.Integer,
	'created_at': fields.DateTime,
	'category_game': fields.Nested(category_game_fields),
	'gallery': fields.Nested(gallery_fields, allow_null=True)
}
product_minimized_fields = {'id': fields.Integer, 'title': fields.String}

country_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'flag': fields.Nested(image_fields, allow_null=True)
}

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	'country': fields.Nested(country_fields),
	'created_at': fields.DateTime,
	'profile_picture': fields.Nested(image_fields, allow_null=True)
}

review_fields = {
	'id': fields.Integer,
	'author': fields.Nested(user_fields),
	'product': fields.Nested(product_minimized_fields),
	'rating': fields.Integer,
	'comment': fields.String,
	'created_at': fields.DateTime,
	'gallery': fields.Nested(gallery_fields, allow_null=True)
}

cart_item_fields = {
	'id': fields.Integer,
	'quantity': fields.Integer,
	'product': fields.Nested(product_minimized_fields)
}

cart_fields = {
	'id': fields.Integer,
	'user': fields.Nested(user_fields),
	'items': fields.Nested(cart_item_fields, allow_null=True)
}