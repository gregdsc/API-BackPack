from Source.Point.Model import *
from Source.Point.Model.model_point import Point_picture
from Source.User.Model.model_user import *

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from cloudinary import uploader
import re
from Source.Point.View.point_user_field import *
import datetime
from Source.Authentification.Auth import *
from Source.Point.Model.model_point import *


class Point_filtre(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)
    parser.add_argument('rank', type=int)

    @marshal_with(interest_field)
    def get(self, type):
        pois = session.query(Interest_point).filter(Interest_point.type == type).all()
        if not pois:
            abort(404, message="poi {} doesn't exist".format(type))
        return pois