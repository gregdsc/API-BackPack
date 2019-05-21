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


class ActivitySpeed(Resource):

    @authToken.login_required
    @marshal_with(speed_fields)
    def get(self):
        speed_date = session.query(Activity).order_by(Activity.id.desc()).all()
        if not speed_date:
            abort(404, message="Please enter an activity with speed before")
        return speed_date, 200, {'Access-Control-Allow-Origin': '*'}

    @authToken.login_required
    @marshal_with(speed_fields)
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


class ActivitySpeedMax(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        speeds = session.query(Activity).order_by(Activity.speed.desc()).first()
        if not speeds:
            abort(404, message="Please enter an activity with speed before")
        return speeds, 200, {'Access-Control-Allow-Origin': '*'}


class ActivitySpeedDesc(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        speeds = session.query(Activity).order_by(Activity.speed.desc()).all()
        if not speeds:
            abort(404, message="Please enter an activity with speed before")
        return speeds, 200, {'Access-Control-Allow-Origin': '*'}


class ActivitySpeedMin(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        speeds = session.query(Activity).order_by(Activity.speed.asc()).first()
        if not speeds:
            abort(404, message="Please enter an activity with speed before")
        return speeds, 200, {'Access-Control-Allow-Origin': '*'}