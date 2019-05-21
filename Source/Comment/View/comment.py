from flask import g
import json
import re
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
import datetime
from Source.Comment.View.fields_comment import *
from Source.Point.View.interest_point import *
from Source.Comment.Model.model_comment import *
authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()


class comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str)
    parser.add_argument('id', type=int)
    parser.add_argument('rank', type=int)

    @marshal_with(champs)
    def get(self):
        comment = session.query(Point).all()
        return comment, 201

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        details = parsed_args['description']
        rank = parsed_args['rank']
        date = datetime.datetime.now()
        id = parsed_args['id']
        comment = Comment(creation=date, details=details, rank=rank, point_id=id, username=g.current_user.username,
                          derniere_modification=date)
        session.add(comment)
        session.commit()
        return 201

    @authToken.login_required
    def put(self, id):
        parsed_args = self.parser.parse_args()

        comment = session.query(Comment).filter(Comment.id == id).filter(Comment.username == g.current_user.username)\
            .first()
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

class comment_point(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str)
    parser.add_argument('id', type=int)
    parser.add_argument('rank', type=int)

    @marshal_with(champs)
    def get(self, id_poi):
        comment = session.query(Interest_point).filter(Interest_point.id == id_poi).all()
        return comment, 201
