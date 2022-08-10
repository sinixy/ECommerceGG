from flask_restful import Resource, marshal
from ..auth import login_required
from ..models import db, Cart, CartItem, Product
from ..common.inputs import cart_add_item_parser, cart_delete_item_parser
from ..common.outputs import cart_fields, cart_item_fields


def access_required(f):
	def decorator(current_user, cart_id=0):
		cart = Cart.query.get(cart_id)
		if not cart:
			return {'status': 'error', 'message': 'No such cart'}, 404
		if cart.user_id != current_user.id:
			return {'status': 'error', 'message': 'You cannot access this cart'}, 403
		return f(current_user, cart)
	return decorator


class CartResource(Resource):
	method_decorators = [access_required, login_required]

	def get(self, current_user, cart):
		return {'data': {'cart': marshal(cart, cart_fields)}, 'status': 'success'}

	def post(self, current_user, cart):
		# add an item to the cart
		args = cart_add_item_parser.parse_args()
		quantity = args['quantity']
		if quantity <= 0:
			return {'data': {'quantity': 'Quantity must be greater than zero'}, 'status': 'fail'}, 400

		product = Product.query.get(args['productId'])
		if not product:
			return {'status': 'error', 'message': 'No such product'}, 404

		new_item = CartItem.query.filter_by(cart=cart, product=product).first()
		if new_item:
			new_item.quantity += quantity
		else:
			new_item = CartItem(quantity=quantity, cart=cart, product=product)
			db.session.add(new_item)
		db.session.commit()
		db.session.refresh(new_item)

		return {'data': {'newItem': marshal(new_item, cart_item_fields)}, 'status': 'success'}, 201

	def delete(self, current_user, cart):
		# delete an item from the cart or clear the cart
		args = cart_delete_item_parser.parse_args()
		if args['productId']:
			# delete only one item
			product = Product.query.get(args['productId'])
			if not product:
				return {'status': 'error', 'message': 'No such product'}, 404

			item = CartItem.query.filter_by(cart=cart, product=product).first()
			if not item:
				return {'status': 'error', 'message': 'No such cart item'}, 404

			db.session.delete(item)
			db.session.commit()

			return {'data': None, 'status': 'success'}

		else:
			# delete all items
			CartItem.query.filter_by(cart=cart).delete()
			db.session.commit()
			return {'data': None, 'status': 'success'}