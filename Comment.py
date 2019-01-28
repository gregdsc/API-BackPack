from flask import g
from db import session
import json
import re
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from manage import *
from resources import InterestPointRessource, InterestPointListRessource
import datetime

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()

champs_comment = {
    'username': fields.String,
    'details': fields.String,
    'date': fields.DateTime(attribute='creation')
}

#'users': fields.List(fields.String(attribute='username')),

champs = {
    'comment': fields.Nested(champs_comment)
}


class comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str)
    parser.add_argument('id', type=int)
    @marshal_with(champs)
    def get(self, id_poi):
        resto_ville = session.query(InterestPoint).filter(InterestPoint.id == id_poi).all()
        print(resto_ville)
        return resto_ville, 201

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        details = parsed_args['description']
        date = datetime.datetime.now()
        id = parsed_args['id']
        comment = Comment(creation=date, details=details, point_id=id, username=g.user.username)

        session.add(comment)
        session.commit()
        return 201


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True
