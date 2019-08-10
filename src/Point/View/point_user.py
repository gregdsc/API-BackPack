from flask import g
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Authentification.authentification import authToken
from src.Point.View.point_user_field import interest_field
from src.Point.Model.model_point import InterestPoint
from src.Configuration.session import session


class UserPoi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)

    @marshal_with(interest_field)
    @authToken.login_required
    def get(self):
        user_pois = session.query(InterestPoint).filter(InterestPoint.user_id == g.current_user.id).all()
        return user_pois

    @authToken.login_required
    def delete(self, id_point):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id_point).filter(InterestPoint.user_id ==
                                                                                   g.current_user.id).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id_point))
        session.delete(poi)
        session.commit()
        return {}, 204
