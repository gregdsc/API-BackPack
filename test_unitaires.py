#!/usr/bin/env python

import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from settings import DB_URI
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from db import session
from flask_cors import CORS
from sqlalchemy import ForeignKey

import base64



app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = "I7QkQImQ6468QJkKQJ434QHJHFLSssjd"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from manage import *

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.hash_password('cat')
        self.assertFalse(u.verify_password('dog'))
        self.assertTrue(u.verify_password('cat'))

class UserVueCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user(self):
        # the test client can request a route
        self.user = User(username='joe@theodo.fr',
                         password_hash='supermotdepasse')
        response = self.client.get(
            '/user/%s' % self.user.id,
        )

        self.assertEqual(response.status_code, 404)

    def get_api_headers(self, username, password):
            return {
                'Authorization': 'Basic ' + base64.b64encode(
                   (username + ':' + password).encode('utf-8')).decode('utf-8')
            }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password'))
        self.assertEqual(response.status_code, 404)

    def test_no_auth(self):
        response = self.client.get('/api/v1/posts/',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_bad_auth(self):
        u = User(username='john@example.com', password_hash='cat')
        db.session.add(u)
        db.session.commit()

        # authenticate with bad password
        response = self.client.get(
            '/login/',
            headers=self.get_api_headers('john@example.com', 'dog'))
        self.assertEqual(response.status_code, 404)

    def test_token_auth(self):
        # add a user

        u = User(username='john@example.com', password_hash='cat')
        db.session.add(u)
        db.session.commit()

        # issue a request with a bad token
        response = self.client.get(
            '/users/1',
            headers=self.get_api_headers('bad-token', ''))
        self.assertEqual(response.status_code, 404)

        # get a token
        response = self.client.get(
            '/login',
            headers=self.get_api_headers('john@example.com', 'cat'))
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
