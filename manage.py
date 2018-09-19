from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import DB_URI
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from db import session
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = "I7QkQImQ6468QJkKQJ434QHJHFLSssjd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    password_hash = db.Column(db.String(255))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = session.query(User).filter(User.id == data['id']).first()
        return user


class ImageUrls(db.Model):
    __tablename__ = 'imageUrls'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    poiName = db.Column(db.String)


class InterestPoint(db.Model):
    __tablename__ = 'interestPoint'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    userName = db.Column(db.String(255))
    type = db.Column(db.String(255))
    imageUrls = []


if __name__ == '__main__':
    manager.run()
