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
    'pas': fields.Integer,
    'km': fields.Float,
    'calorie': fields.Float,
    'speed': fields.Float,
    'type': fields.String,
    'uri': fields.Url('activity', absolute=True),
}

calorie_fields = {
    'id': fields.Integer,
    'calorie': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('calorie', absolute=True),
}

calorie_field = {
    'calorie': fields.Float,
    'start_time': fields.DateTime
}

speed_fields = {
    'id': fields.Integer,
    'speed': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('speed', absolute=True),
}

speed_field = {
    'speed': fields.Float,
    'start_time': fields.DateTime
}

pas_fields = {
    'id': fields.Integer,
    'pas': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('pas', absolute=True),
}

pas_field = {
    'pas': fields.Float,
    'start_time': fields.DateTime
}

km_fields = {
    'id': fields.Integer,
    'km': fields.Float,
    'start_time': fields.DateTime,
    'uri': fields.Url('km', absolute=True),
}

km_field = {
    'km': fields.Float,
    'start_time': fields.DateTime
}

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()


# ACTIVITIES #

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


# ACTIVITY CALORIE #


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


# ACTIVITY SPEEDS #


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


# ACTIVITY PAS #

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

    # ACTIVITY KM #


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


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True
