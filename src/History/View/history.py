from flask import g
from flask_restful import Resource
from flask_restful import marshal_with
from src.Authentification.authentification import authToken
from src.Point.View.interest_point import Point
from src.History.View.fields_history import interest_field
from src.Point.Model.model_point import InterestPoint
from src.Configuration.session import session

class HistoriqueDate(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(Point).filter(Point.user_id == g.user.id).order_by(InterestPoint.date.asc()).all()
        return pois, 201


class HistoriqueRank(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).filter(InterestPoint.user_id == g.user.id) \
            .order_by(InterestPoint.rank.asc()).all()
        return pois, 201
