import flask_sqlalchemy 
import flask_migrate
from .settings import app


db = flask_sqlalchemy.SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db.init_app(app)

migration = flask_migrate.Migrate(app = app, db = db, directory = 'app/migrations')

