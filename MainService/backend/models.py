from . import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
	__tablename__ = 'User'

	id = db.Column(db.Integer,  primary_key=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(128), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	country_id = db.Column(db.Integer, db.ForeignKey('Country.id', ondelete='SET NULL'), nullable=True)
	country = db.relationship('Country', backref='users')
	role_id = db.Column(db.Integer, db.ForeignKey('Role.id', ondelete='CASCADE'), nullable=False)
	role = db.relationship('Role', backref='users')
	cart = db.relationship('Cart', backref='user', uselist=False)
	profile_picture_id = db.Column(db.Integer, db.ForeignKey('Image.id', ondelete='SET NULL'), nullable=True, default=None)
	profile_picture = db.relationship('Image', uselist=False)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class Role(db.Model):
	__tablename__ = 'Role'

	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	description = db.Column(db.String(256), nullable=False, default='')


class Country(db.Model):
	__tablename__ = 'Country'

	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	flag_id = db.Column(db.Integer, db.ForeignKey('Image.id', ondelete='SET NULL'), nullable=True, default=None)
	flag = db.relationship('Image', uselist=False)


class Cart(db.Model):
	__tablename__ = 'Cart'

	id = db.Column(db.Integer,  primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)


class CartItem(db.Model):
	__tablename__ = 'CartItem'

	id = db.Column(db.Integer,  primary_key=True)
	quantity = db.Column(db.Integer, nullable=False, default=1)
	cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id', ondelete='CASCADE'), nullable=False)
	cart = db.relationship('Cart', backref='items')
	product_id = db.Column(db.Integer, db.ForeignKey('Product.id', ondelete='CASCADE'), nullable=False)
	product = db.relationship('Product')


class Product(db.Model):
	__tablename__ = 'Product'

	id = db.Column(db.Integer,  primary_key=True)
	title = db.Column(db.String(128), nullable=False, unique=True)
	description = db.Column(db.Text, nullable=False, default='')
	price = db.Column(db.Float, nullable=False)
	available_quantity = db.Column(db.Integer, nullable=False, default=1)
	min_quantity = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	category_game_id = db.Column(db.Integer, db.ForeignKey('CategoryGame.id', ondelete='CASCADE'), nullable=False)
	category_game = db.relationship('CategoryGame', backref='products')
	gallery_id = db.Column(db.Integer, db.ForeignKey('Gallery.id', ondelete='SET NULL'), nullable=True, default=None)
	gallery = db.relationship('Gallery', uselist=False)


class Category(db.Model):
	__tablename__ = 'Category'

	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	icon_id = db.Column(db.Integer, db.ForeignKey('Image.id', ondelete='SET NULL'), nullable=True, default=None)
	icon = db.relationship('Image', uselist=False)


class Game(db.Model):
	__tablename__ = 'Game'

	id = db.Column(db.Integer,  primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	icon_id = db.Column(db.Integer, db.ForeignKey('Image.id', ondelete='SET NULL'), nullable=True, default=None)
	icon = db.relationship('Image', uselist=False)


class CategoryGame(db.Model):
	__tablename__ = 'CategoryGame'

	id = db.Column(db.Integer,  primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('Category.id', ondelete='CASCADE'), nullable=False)
	game_id = db.Column(db.Integer, db.ForeignKey('Game.id', ondelete='CASCADE'), nullable=False)


class Review(db.Model):
	__tablename__ = 'Review'

	id = db.Column(db.Integer,  primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
	author = db.relationship('User', backref='reviews')
	product_id = db.Column(db.Integer, db.ForeignKey('Product.id', ondelete='CASCADE'), nullable=False)
	product = db.relationship('Product', backref='reviews')
	rating = db.Column(db.Integer, nullable=False, default=5)
	comment = db.Column(db.Text, nullable=False, default='')
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	gallery_id = db.Column(db.Integer, db.ForeignKey('Gallery.id', ondelete='SET NULL'), nullable=True, default=None)
	gallery = db.relationship('Gallery', uselist=False)


class Gallery(db.Model):
	__tablename__ = 'Gallery'

	id = db.Column(db.Integer,  primary_key=True)
	type = db.Column(db.String(128), nullable=False, default='')
	images = db.relationship('Image', backref='gallery')


class Image(db.Model):
	__tablename__ = 'Image'

	id = db.Column(db.Integer,  primary_key=True)
	url = db.Column(db.String(512), nullable=False, unique=True)
	gallery_id = db.Column(db.Integer, db.ForeignKey('Gallery.id', ondelete='CASCADE'), nullable=True, default=None)
