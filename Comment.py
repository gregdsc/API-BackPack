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
    'id': fields.Integer,
    'username': fields.String,
    'details': fields.String,
    'rank': fields.Integer,
    'date': fields.DateTime(attribute='creation'),
    'last modification': fields.DateTime(attribute='derniere_modification')
}

#'users': fields.List(fields.String(attribute='username')),

champs = {
    'comment': fields.Nested(champs_comment)
}


class comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str)
    parser.add_argument('id', type=int)
    parser.add_argument('rank', type=int)

    @marshal_with(champs)
    def get(self, id_poi):
        comment = session.query(InterestPoint).filter(InterestPoint.id == id_poi).all()
        return comment, 201

    @marshal_with(champs)
    def get(self):
        comment = session.query(InterestPoint).all()
        return comment, 201

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        details = parsed_args['description']
        rank = parsed_args['rank']
        date = datetime.datetime.now()
        id = parsed_args['id']
        comment = Comment(creation=date, details=details, rank=rank, point_id=id, username=g.user.username, derniere_modification=date)
        session.add(comment)
        session.commit()
        return 201

    def put(self, id):
        parsed_args = self.parser.parse_args()

        comment = session.query(Comment).filter(Comment.id == id).first()
        date = datetime.datetime.now()
        if parsed_args['description'] is not None:
            comment.details = parsed_args['description']
        if parsed_args['rank'] is not None:
            comment.rank = parsed_args['rank']
        comment.derniere_modification = date
        session.add(comment)
        session.commit()
        return {}, 201

    def delete(self, id):
        comment = session.query(Comment).filter(Comment.id == id).first()
        session.delete(comment)
        session.commit()
        return {}, 204

@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True
