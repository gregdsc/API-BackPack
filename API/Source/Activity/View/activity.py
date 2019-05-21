from flask import g
from Source.Configuration.Session import *
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from Source.Authentification.Bearer import *
from Source.Activity.View.activity_fields import *
from Source.Activity.Model.model_activity import *

class ActivityResource(Resource):
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
        pas = parsed_args['pas']
        km = parsed_args['km']
        calorie = parsed_args['calorie']
        speed = parsed_args['speed']
        type = parsed_args['type']

        if name is None or start_time is None or end_time is None or pas is None or km is None or calorie \
                is None or speed is None or type is None:
            abort(400, message="Missing arguments")
        activity = Activity(name=name, start_time=start_time, end_time=end_time,
                            pas=pas, km=km, calorie=calorie, speed=speed, type=type,
                            username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}
