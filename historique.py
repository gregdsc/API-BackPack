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


interest_field = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'lat': fields.Float,
    'long': fields.Float,
    'userName': fields.String,
    'type': fields.String,
    'rank': fields.Integer,
    'imageUrls': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('poi', absolute=True),
}


class historique_date(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).order_by(InterestPoint.date.asc()).all()
        return pois, 201

class historique_rank(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).order_by(InterestPoint.rank.asc()).all()
        return pois, 201

@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True
