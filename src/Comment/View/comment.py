from flask import g
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from src.Authentification.authentification import authToken
from src.Configuration.session import session
from src.Comment.View.fields_comment import champs
from src.Point.View.interest_point import Point, InterestPoint
from src.Comment.Model.model_comment import Comment
import datetime


class UserComment(Resource):
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
        id_point = parsed_args['id']
        comment = Comment(creation=date, details=details, rank=rank, point_id=id_point,
                          username=g.current_user.username, derniere_modification=date)
        session.add(comment)
        session.commit()
        return 201

    @authToken.login_required
    def put(self, id_comment):
        parsed_args = self.parser.parse_args()

        comment = session.query(Comment).filter(Comment.id == id_comment).filter(Comment.username ==
                                                                                 g.current_user.username) \
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

    def delete(self, id_comment):
        comment = session.query(Comment).filter(Comment.id == id_comment).first()
        session.delete(comment)
        session.commit()
        return {}, 204


class CommentPoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str)
    parser.add_argument('id', type=int)
    parser.add_argument('rank', type=int)

    @marshal_with(champs)
    def get(self, id_poi):
        comment = session.query(InterestPoint).filter(InterestPoint.id == id_poi).all()
        return comment, 201
