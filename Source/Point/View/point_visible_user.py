from Moderation_images.moderate_images import Dectection
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
from Source.User.View.user import *


class Point_visible_user(Resource):

    @marshal_with(interest_field)
    def get(self, id):
        poi_visible = session.query(Interest_point).filter(Interest_point.user_id == id).\
            filter(Interest_point.visible == True).all()
        if not poi_visible:
            abort(401, message='No point for this user')
        return poi_visible
