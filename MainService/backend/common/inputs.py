from flask_restful import reqparse


# === Product ===
product_parser = reqparse.RequestParser(bundle_errors=True)
product_parser.add_argument('q', type=str)
product_parser.add_argument('category', type=str)
product_parser.add_argument('game', type=str)
product_parser.add_argument('minPrice', type=float)
product_parser.add_argument('maxPrice', type=float)

# === Review ===
review_search_parser = reqparse.RequestParser(bundle_errors=True)
review_search_parser.add_argument('productId', type=int)
review_search_parser.add_argument('authorId', type=int)

review_create_parser = reqparse.RequestParser(bundle_errors=True)
review_create_parser.add_argument('authorId', type=int, required=True)
review_create_parser.add_argument('productId', type=int, required=True)
review_create_parser.add_argument('rating', type=int, required=True)
review_create_parser.add_argument('comment', type=str, required=True)
# review_create_parser.add_argument('gallery')

review_edit_parser = reqparse.RequestParser(bundle_errors=True)
review_edit_parser.add_argument('rating', type=int, required=True)
review_edit_parser.add_argument('comment', type=str, required=True)
# review_edit_parser.add_argument('gallery')

# === Cart ===
cart_add_item_parser = reqparse.RequestParser(bundle_errors=True)
cart_add_item_parser.add_argument('quantity', type=int, required=True)
cart_add_item_parser.add_argument('productId', type=int, required=True)

cart_delete_item_parser = reqparse.RequestParser()
cart_delete_item_parser.add_argument('productId', type=int)