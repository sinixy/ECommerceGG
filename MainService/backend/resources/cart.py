from flask_restful import Resource, marshal
from ..models import db, Cart, CartItem, Product
from ..common.inputs import cart_add_item_parser, cart_delete_item_parser
from ..common.outputs import cart_fields, cart_item_fields


class CartResource(Resource):
	def get(self, cart_id):
		cart = Cart.query.get(cart_id)
		if cart:
			return marshal(cart, cart_fields), 200
		else:
			return {'data': {}, 'errors': ['No such cart'], 'status': 'error'}, 404

	def post(self, cart_id):
		# add an item to the cart
		cart = Cart.query.get(cart_id)
		if not cart:
			return {'data': {}, 'errors': ['No such cart'], 'status': 'error'}, 404

		args = cart_add_item_parser.parse_args(strict=True)

		quantity = args['quantity']
		if quantity <= 0:
			return {'data': {}, 'errors': ['Quantity must be greater than zero'], 'status': 'error'}, 400

		product = Product.query.get(args['productId'])
		if not product:
			return {'data': {}, 'errors': ['No such product'], 'status': 'error'}, 404

		new_item = CartItem.query.filter_by(cart=cart, product=product).first()
		if new_item:
			new_item.quantity += quantity
		else:
			new_item = CartItem(quantity=quantity, cart=cart, product=product)
			db.session.add(new_item)
		db.session.commit()
		db.session.refresh(new_item)

		return {'data': marshal(new_item, cart_item_fields), 'errors': [], 'status': 'ok'}, 201

	def delete(self, cart_id):
		# delete an item from the cart or clear the cart
		cart = Cart.query.get(cart_id)
		if not cart:
			return {'data': {}, 'errors': ['No such cart'], 'status': 'error'}, 404

		args = cart_delete_item_parser.parse_args(strict=True)
		if args['productId']:
			# delete only one item
			product = Product.query.get(args['productId'])
			if not product:
				return {'data': {}, 'errors': ['No such product'], 'status': 'error'}, 404

			item = CartItem.query.filter_by(cart=cart, product=product).first()
			if not item:
				return {'data': {}, 'errors': ['No such cart item'], 'status': 'error'}, 404

			db.session.delete(item)
			db.session.commit()

			return {'data': {}, 'errors': [], 'status': 'ok'}, 204
		else:
			# delete all items
			CartItem.query.filter_by(cart=cart).delete()
			db.session.commit()
			return {'data': {}, 'errors': {}, 'status': 'ok'}, 204