from src.Configuration.session import session
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Point.View.point_user_field import interest_field
from src.Point.Model.model_point import InterestPoint


class PointVisibleUser(Resource):

    @marshal_with(interest_field)
    def get(self, id):
        poi_visible = session.query(InterestPoint).filter(InterestPoint.user_id == id). \
            filter(InterestPoint.visible == True).all()
        if not poi_visible:
            abort(401, message='No point for this user')
        return poi_visible
