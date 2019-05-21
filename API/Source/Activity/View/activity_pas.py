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


class ActivityPas(Resource):

    @authToken.login_required
    @marshal_with(pas_fields)
    def get(self):
        pas = session.query(Activity).order_by(Activity.pas.desc()).all()
        if not pas:
            abort(404, message="Please enter an activity with Number Pas before")
        return pas, 200, {'Access-Control-Allow-Origin': '*'}

    @authToken.login_required
    @marshal_with(pas_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        pas = parsed_args['pas']
        start_time = parsed_args['start_time']
        if start_time is None or pas is None:
            abort(400, message="Missing arguments")
        activity = Activity(pas=pas, start_time=start_time, username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityPasMax(Resource):

    @authToken.login_required
    @marshal_with(pas_field)
    def get(self):
        pas = session.query(Activity).order_by(Activity.pas.desc()).first()
        if not pas:
            abort(404, message="Please enter an activity with Number Pas before")
        return pas, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityPasDesc(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        pas = session.query(Activity).order_by(Activity.pas.desc()).all()
        if not pas:
            abort(404, message="Please enter an activity with Number Pas before")
        return pas, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityPasMin(Resource):

    @authToken.login_required
    @marshal_with(speed_field)
    def get(self):
        pas = session.query(Activity).order_by(Activity.pas.asc()).first()
        if not pas:
            abort(404, message="Please enter an activity with Number Pas before")
        return pas, 200, {'Access-Control-Allow-Origin': '*'}