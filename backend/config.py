import os
from datetime import timedelta


class Config:
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'no_secret')
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
	JWT_TOKEN_LOCATION = ['cookies']
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
	DEBUG = True
	JWT_COOKIE_SECURE = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class ProdConfig(Config):
	DEBUG = False
	JWT_COOKIE_SECURE = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')


config = {
	'development': DevConfig,
	'production': ProdConfig
}