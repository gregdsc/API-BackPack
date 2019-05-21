from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from Source.User.Model.model_user import *

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()


@authBasic.verify_password
def verify_password(mail, password):
    user = User.query.filter_by(mail=mail).first()
    if user is None:
        return False
    g.current_user = user
    return user.verifie_mdp(password)


@authToken.verify_token
def verify_token(token):
    g.current_user = User.verify_auth_token(token) if token else None
    return g.current_user is not None, True

