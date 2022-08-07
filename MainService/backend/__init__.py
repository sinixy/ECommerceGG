from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_backend_app(app_config):
	app = Flask(__name__)
	app.config.from_object(app_config)
	
	db.init_app(app)

	from .api import api_blueprint
	app.register_blueprint(api_blueprint)

	from .auth import auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app