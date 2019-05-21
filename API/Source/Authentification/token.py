from flask import g
from flask_restful import Resource
from Source.Authentification.Bearer import *

class GetToken(Resource):
    @authBasic.login_required
    def get(self):
        token = g.current_user.generate_auth_token(expiration=10000)
        return {'id_user': g.current_user.id,
                'token': token.decode('ascii')
                }

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
    g.current_user = User.verifie_auth_token(token) if token else None
    return g.current_user is not None, True

