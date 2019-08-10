from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from configuration import config
from flask_cors import CORS

db = SQLAlchemy()
mail = Mail()
cors = CORS()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app)
    from app import api
    api.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
    return app
