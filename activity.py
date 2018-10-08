from flask import g
from db import session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from manage import Activity, User

activity_field = {
    'id': fields.Integer,
    'name': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'count': fields.Integer,
    'distance': fields.Float,
    'calorie': fields.Float,
    'speed': fields.Float,
    'type': fields.String,
    'uri': fields.Url('activity', absolute=True),
}

calorie_field = {
    'id': fields.Integer,
    'calorie': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('calorie', absolute=True),
}

speed_field = {
    'id': fields.Integer,
    'speed': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('speed', absolute=True),
}

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()


class ActivityResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('start_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('count', type=int)
    parser.add_argument('distance', type=float)
    parser.add_argument('calorie', type=float)
    parser.add_argument('speed', type=float)
    parser.add_argument('type', type=str)

    @marshal_with(activity_field)
    @authBasic.login_required
    def get(self):
        activities = session.query(Activity).all()
        if not activities:
            abort(404, message="Please enter an activity before")
        return activities, 200, {'Access-Control-Allow-Origin': '*'}

    @authToken.login_required
    @marshal_with(activity_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        start_time = parsed_args['start_time']
        end_time = parsed_args['end_time']
        count = parsed_args['count']
        distance = parsed_args['distance']
        calorie = parsed_args['calorie']
        speed = parsed_args['speed']
        type = parsed_args['type']

        if name is None or start_time is None or end_time is None or count is None or distance is None or calorie \
                is None or speed is None or type is None:
            abort(400, message="Missing arguments")
        activity = Activity(name=name, start_time=start_time, end_time=end_time,
                            count=count, distance=distance, calorie=calorie, speed=speed, type=type,
                            username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityCalorie(Resource):

    @authToken.login_required
    @marshal_with(calorie_field)
    def get(self):
        calorie_date = session.query(Activity).all()
        if not calorie_date:
            abort(404, message="Please enter an activity with calorie before")
        return calorie_date

    @authToken.login_required
    @marshal_with(calorie_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        calorie = parsed_args['calorie']
        start_time = parsed_args['start_time']
        if start_time is None or calorie is None:
            abort(400, message="Missing arguments")
        activity = Activity(calorie=calorie,start_time=start_time, username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}

class ActivitySpeed(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        speed_date = session.query(Activity).all()
        if not speed_date:
            abort(404, message="Please enter an activity with calorie before")
        return speed_date

    @authToken.login_required
    @marshal_with(speed_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        speed = parsed_args['speed']
        start_time = parsed_args['start_time']
        if start_time is None or speed is None:
            abort(400, message="Missing arguments")
        activity = Activity(speed=speed, start_time=start_time, username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True