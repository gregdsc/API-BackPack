
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from configuration import config
from flask_cors import CORS


db = SQLAlchemy()
mail = Mail()
cors = CORS()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    return app

