import os


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY', 'no_secret')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class ProdConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')


config = {
	'development': DevConfig,
	'production': ProdConfig
}