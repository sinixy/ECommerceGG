from flask_restful import Resource, marshal
from ..models import db, Review, Product, User
from ..common.inputs import review_search_parser, review_create_parser, review_edit_parser
from ..common.outputs import review_fields


class ReviewResource(Resource):
	def get(self, review_id=None):
		if review_id:
			review = Review.query.get(review_id)
			if review:
				return marshal(review, review_fields), 200
			else:
				return {'data': {}, 'errors': ['No such review'], 'status': 'error'}, 404
		else:
			args = review_search_parser.parse_args(strict=True)
			query = Review.query

			if args['productId']:
				product = Product.query.get(args['productId'])
				if not product:
					return {'data': [], 'errors': ['No such product'], 'status': 'error'}, 404
				query = query.filter_by(product=product)
			if args['authorId']:
				author = User.query.get(args['authorId'])
				if not author:
					return {'data': [], 'errors': ['No such user'], 'status': 'error'}, 404
				query = query.filter_by(author=author)

			return {'data': marshal(query.all(), review_fields), 'errors': [], 'status': 'ok'}, 200

	def post(self):
		args = review_create_parser.parse_args(strict=True)

		author = User.query.get(args['authorId'])
		if not author:
			return {'data': {}, 'errors': ['No such user'], 'status': 'error'}, 404

		product = Product.query.get(args['productId'])
		if not product:
			return {'data': {}, 'errors': ['No such product'], 'status': 'error'}, 404

		rating = args['rating']
		if rating > 5 or rating < 1:
			return {'data': {}, 'errors': ['Invalid rating range'], 'status': 'error'}, 400

		new_review = Review(author=author, product=product, rating=rating, comment=args['comment'])
		db.session.add(new_review)
		db.session.commit()
		db.session.refresh(new_review)

		return {'data': marshal(new_review, review_fields), 'errors': [], 'status': 'ok'}, 201

	def patch(self, review_id=None):
		if review_id:
			review = Review.query.get(review_id)
			if not review:
				return {'data': {}, 'errors': ['No such review'], 'status': 'error'}, 404

			args = review_edit_parser.parse_args(strict=True)

			rating = args['rating']
			if rating > 5 or rating < 1:
				return {'data': {}, 'errors': ['Invalid rating range'], 'status': 'error'}, 400

			comment = args['comment']
			if len(comment) == 0:
				return {'data': {}, 'errors': ['Comment cannot be empty'], 'status': 'error'}, 400

			review.rating = rating
			review.comment = comment
			db.session.commit()

			return {'data': {}, 'errors': [], 'status': 'ok'}, 204
		else:
			return {'data': {}, 'errors': ['Review not specified'], 'status': 'error'}, 400

	def delete(self, review_id=None):
		if review_id:
			review = Review.query.get(review_id)
			if not review:
				return {'data': {}, 'errors': ['No such review'], 'status': 'error'}, 404

			db.session.delete(review)
			db.session.commit()

			return {'data': {}, 'errors': [], 'status': 'ok'}, 204
		else:
			return {'data': {}, 'errors': ['Review not specified'], 'status': 'error'}, 400