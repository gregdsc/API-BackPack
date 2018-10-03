from flask import g

from manage import Activity, User
from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

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
    def get(self):
        activities = session.query(Activity).all()
        return activities, 201, {'Access-Control-Allow-Origin': '*'}

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
        return activity, 201, {'Access-Control-Allow-Origin': '*'}


    @authToken.verify_token
    def verify_token(token):
        user = User.verify_auth_token(token)
        if user is None:
            return False
        g.user = user
        return True