from flask_restful import reqparse


# === Game ===
game_parser = reqparse.RequestParser(bundle_errors=True)
game_parser.add_argument('categoryId', type=int)

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

review_create_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
review_create_parser.add_argument('productId', type=int, required=True)
review_create_parser.add_argument('rating', type=int, required=True)
review_create_parser.add_argument('comment', type=str, required=True)
# review_create_parser.add_argument('gallery')

review_edit_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
review_edit_parser.add_argument('rating', type=int, required=True)
review_edit_parser.add_argument('comment', type=str, required=True)
# review_edit_parser.add_argument('gallery')

# === Cart ===
cart_add_item_parser = reqparse.RequestParser(bundle_errors=True)
cart_add_item_parser.add_argument('quantity', type=int, required=True)
cart_add_item_parser.add_argument('productId', type=int, required=True)

cart_delete_item_parser = reqparse.RequestParser()
cart_delete_item_parser.add_argument('productId', type=int)

# === Token ===
token_create_parser = reqparse.RequestParser(bundle_errors=True)
token_create_parser.add_argument('username', type=str, required=True)
token_create_parser.add_argument('password', type=str, required=True)

# === User ===
user_create_parser = reqparse.RequestParser(bundle_errors=True)
user_create_parser.add_argument('username', type=str, required=True)
user_create_parser.add_argument('password', type=str, required=True)
user_create_parser.add_argument('email', type=str, required=True)
user_create_parser.add_argument('countryId', type=int, required=True)
# user_create_parser.add_argument('profile_picture')

user_edit_parser = user_create_parser.copy()
user_edit_parser.remove_argument('password')
user_edit_parser.add_argument('oldPassword', type=str, required=True)
user_edit_parser.add_argument('newPassword', type=str, required=True)