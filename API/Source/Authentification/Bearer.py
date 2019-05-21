from flask_restful import Resource
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import abort
from flask_restful import reqparse
from Source.User.Model.model_user import *

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()

@authBasic.verify_password
def verify_password(mail, password):
    user = User.query.filter_by(mail=mail).first()
    if user is None:
        return False
    g.current_user = user
    return user.verify_password(password)

@authToken.verify_token
def verify_token(token):
    g.current_user = User.verifie_auth_token(token) if token else None
    return g.current_user is not None