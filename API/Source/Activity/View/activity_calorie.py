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


class ActivityCalorie(Resource):

    @authToken.login_required
    @marshal_with(calorie_fields)
    def get(self):
        calorie_date = session.query(Activity).all()
        if not calorie_date:
            abort(404, message="Please enter an activity with calorie before")
        return calorie_date

    @authToken.login_required
    @marshal_with(calorie_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        calorie = parsed_args['calorie']
        start_time = parsed_args['start_time']
        if start_time is None or calorie is None:
            abort(400, message="Missing arguments")
        activity = Activity(calorie=calorie, start_time=start_time, username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}



class ActivityCalorieMax(Resource):

    @authToken.login_required
    @marshal_with(calorie_field)
    def get(self):
        Calorie = session.query(Activity).order_by(Activity.calorie.desc()).first()
        if not Calorie:
            abort(404, message="Please enter an activity with calorie before")
        return Calorie, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityCalorieDesc(Resource):

    @authToken.login_required
    @marshal_with(calorie_field)
    def get(self):
        Calorie = session.query(Activity).order_by(Activity.calorie.desc()).all()
        if not Calorie:
            abort(404, message="Please enter an activity with calorie before")
        return Calorie, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityCalorieMin(Resource):

    @authToken.login_required
    @marshal_with(calorie_field)
    def get(self):
        Calorie = session.query(Activity).order_by(Activity.calorie.asc()).first()
        if not Calorie:
            abort(404, message="Please enter an activity with calorie before")
        return Calorie, 200, {'Access-Control-Allow-Origin': '*'}
