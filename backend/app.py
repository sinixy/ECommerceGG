from flask import Flask
from flask_jwt_extended import JWTManager
import os

from db import db, migrate
from config import config


def create_backend_app(app_config):
	app = Flask(__name__)
	jwt = JWTManager()
	app.config.from_object(app_config)
	app.config
	
	db.init_app(app)
	migrate.init_app(app)
	jwt.init_app(app)

	from api import api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/v1')

	from auth import auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	return app


from db import wait_for_db, run_migrations

app = create_backend_app(config[os.environ.get('FLASK_CONFIG', 'development')])

if wait_for_db(app.config['SQLALCHEMY_DATABASE_URI']):
	print('Running migrations...')
	run_migrations(app)

if os.environ.get('POPULATE'):
	from models import populate_db
	print('Populating the db...')
	populate_db()

app.run(host='0.0.0.0', port=5000)