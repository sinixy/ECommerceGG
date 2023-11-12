from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import time


db = SQLAlchemy()
migrate = Migrate(db=db)


def wait_for_db(db_uri, retries=10, delay=3):
    engine = create_engine(db_uri)
    for _ in range(retries):
        try:
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            return True
        except OperationalError:
            print("Waiting for database...")
            time.sleep(delay)
    print("Failed to connect to database.")
    return False

def run_migrations(app):
    with app.app_context():
        upgrade()