from flask import g
import json
import re
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import marshal_with
from Source.Authentification.Bearer import *
from Source.Point.View.interest_point import *
from Source.History.View.fields_history import *
from Source.Point.Model.model_point import *

class historique_date(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(Point).filter(Point.user_id == g.user.id).order_by(Interest_point.date.asc()).all()
        return pois, 201

class historique_rank(Resource):

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(Interest_point).filter(Interest_point.user_id == g.user.id)\
            .order_by(Interest_point.rank.asc()).all()
        return pois, 201
