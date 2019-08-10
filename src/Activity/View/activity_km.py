from flask import g
from src.Configuration.session import session
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Authentification.authentification import authToken
from src.Activity.View.activity_fields import km_fields, km_field
from src.Activity.Model.model_activity import Activity


class ActivityKm(Resource):

    @authToken.login_required
    @marshal_with(km_fields)
    def get(self):
        km = session.query(Activity).order_by(Activity.km.desc()).all()
        if not km:
            abort(404, message="Please enter an activity with km before")
        return km, 200, {'Access-Control-Allow-Origin': '*'}

    @authToken.login_required
    @marshal_with(km_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        km = parsed_args['km']
        start_time = parsed_args['start_time']
        if start_time is None or km is None:
            abort(400, message="Missing arguments")
        activity = Activity(km=km, start_time=start_time, username=g.user.username)
        session.add(activity)
        session.commit()
        return activity, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityKmMax(Resource):

    @authToken.login_required
    @marshal_with(km_field)
    def get(self):
        km = session.query(Activity).order_by(Activity.km.desc()).first()
        if not km:
            abort(404, message="Please enter an activity with km before")
        return km, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityKmDesc(Resource):

    @authToken.login_required
    @marshal_with(km_field)
    def get(self):
        km = session.query(Activity).order_by(Activity.km.desc()).all()
        if not km:
            abort(404, message="Please enter an activity with km before")
        return km, 200, {'Access-Control-Allow-Origin': '*'}


class ActivityKmMin(Resource):

    @authToken.login_required
    @marshal_with(km_field)
    def get(self):
        km = session.query(Activity).order_by(Activity.km.asc()).first()
        if not km:
            abort(404, message="Please enter an activity with km before")
        return km, 200, {'Access-Control-Allow-Origin': '*'}
