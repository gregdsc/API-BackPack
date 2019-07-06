from flask import g
from flask_login import current_user
from flask_restful import Resource
from Source.Authentification.Bearer import *

class GetToken(Resource):
    @authBasic.login_required
    def get(self):
        g.user = current_user
        token = g.current_user.generate_auth_token(expiration=10000)
        return {'id_user': g.current_user.id,
                'token': token.decode('ascii')
                }
