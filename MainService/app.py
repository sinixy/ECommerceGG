from backend import create_backend_app, db
from backend.models import *
from config import config
from flask_migrate import Migrate
import os


app = create_backend_app(config[os.environ.get('FLASK_CONFIG', 'development')])
migrate = Migrate(app, db)

if __name__ == '__main__':
	app.run()