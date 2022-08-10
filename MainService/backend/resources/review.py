from flask_restful import Resource, marshal
from ..models import db, Review, Product, User
from ..auth import login_required
from ..common.inputs import review_search_parser, review_create_parser, review_edit_parser
from ..common.outputs import review_fields


def access_required(f):
	def decorator(current_user, review_id=0):
		review = Review.query.get(review_id)
		if not review:
			return {'status': 'error', 'message': 'No such review'}, 404
		if review.author_id != current_user.id:
			return {'status': 'error', 'message': 'You cannot modify this review'}, 403
		return f(current_user, review)
	return decorator

def validate_args(args):
	rating = args['rating']
	if rating > 5 or rating < 1:
		return {'data': {'rating': 'Invalid rating range'}, 'status': 'fail'}, 400
	comment = args['comment']
	if len(comment) == 0:
		return {'data': {'comment': 'Comment cannot be empty'}, 'status': 'fail'}, 400
	return {'status': 'success', 'message': 'ok'}, 200

class ReviewResource(Resource):
	method_decorators = {
		'post': [login_required],
		'patch': [access_required, login_required],
		'delete': [access_required, login_required]
	}

	def get(self, review_id=0):
		if review_id:
			review = Review.query.get(review_id)
			if review:
				return {'data': {'review': marshal(review, review_fields)}, 'status': 'success'}
			else:
				return {'status': 'error', 'message': 'No such review'}, 404
		else:
			args = review_search_parser.parse_args(strict=True)
			query = Review.query

			if args['productId']:
				product = Product.query.get(args['productId'])
				if not product:
					return {'status': 'error', 'message': 'No such product'}, 404
				query = query.filter_by(product=product)
			if args['authorId']:
				author = User.query.get(args['authorId'])
				if not author:
					return {'status': 'error', 'message': 'No such user'}, 404
				query = query.filter_by(author=author)

			return {'data': {'reviews': marshal(query.all(), review_fields)}, 'status': 'success'}

	def post(self, current_user):
		args = review_create_parser.parse_args(strict=True)

		product = Product.query.get(args['productId'])
		if not product:
			return {'status': 'error', 'message': 'No such product'}, 404

		validation = validate_args(args)
		if validation[1] != 200:
			return validation

		new_review = Review(author=current_user, product=product, rating=args['rating'], comment=args['comment'])
		db.session.add(new_review)
		db.session.commit()
		db.session.refresh(new_review)

		return {'data': {'review': marshal(new_review, review_fields)}, 'status': 'success'}, 201

	def patch(self, current_user, review):
		args = review_edit_parser.parse_args(strict=True)

		validation = validate_args(args)
		if validation[1] != 200:
			return validation

		review.rating = args['rating']
		review.comment = args['comment']
		db.session.commit()

		return {'data': None, 'status': 'success'}

	def delete(self, review):
		db.session.delete(review)
		db.session.commit()

		return {'data': None, 'status': 'success'}