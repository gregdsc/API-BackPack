from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Point.View.point_user_field import interest_field
from src.Point.Model.model_point import InterestPoint
from src.Configuration.session import session


class PointFiltre(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)
    parser.add_argument('rank', type=int)

    @marshal_with(interest_field)
    def get(self, type):
        pois = session.query(InterestPoint).filter(InterestPoint.type == type).all()
        if not pois:
            abort(404, message="poi {} doesn't exist".format(type))
        return pois
