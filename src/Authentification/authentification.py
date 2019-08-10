from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from src.User.Model.model_user import User
from src.Configuration.session import session

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()


@authBasic.verify_password
def verify_password(mail, password):
    user = session.query(User).filter(User.mail == mail).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    return True


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.current_user = user
    return True
