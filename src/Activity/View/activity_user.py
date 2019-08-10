from flask import g
from src.Configuration.session import session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Authentification.authentification import authToken
from src.Activity.View.activity_fields import activity_field
from src.Activity.Model.model_activity import Activity


class UserActivity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('start_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('pas', type=int)
    parser.add_argument('km', type=float)
    parser.add_argument('calorie', type=float)
    parser.add_argument('speed', type=float)
    parser.add_argument('type', type=str)

    @authToken.login_required
    @marshal_with(activity_field)
    def get(self):
        activities = session.query(Activity).filter(Activity.username == g.user.username).all()
        if not activities:
            abort(404, message="Please enter an activity before")
        return activities, 200, {'Access-Control-Allow-Origin': '*'}
