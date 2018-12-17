from flask import g

from manage import User, InterestPoint, ImageUrls
from db import session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from cloudinary import uploader

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password_hash': fields.String,
    'uri': fields.Url('user', absolute=True),

}

interest_field = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'lat': fields.Float,
    'long': fields.Float,
    'userName': fields.String,
    'type': fields.String,
    'imageUrls': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('poi', absolute=True),
}


authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()

class User_Poi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)

    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).filter(InterestPoint.userName == g.user.username).all()
        for poi in pois:
            poi.imageUrls = session.query(ImageUrls).filter(ImageUrls.poiName == poi.name).all()
        return pois