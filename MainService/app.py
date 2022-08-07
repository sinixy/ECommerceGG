from backend import create_backend_app, db
from config import config
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()


app = create_backend_app(config[os.environ.get('FLASK_CONFIG', 'development')])
migrate = Migrate(app, db)

if __name__ == '__main__':
	app.run()