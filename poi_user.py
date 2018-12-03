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

    @authToken.login_required
    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).filter(InterestPoint.userName == g.user.username).all()
        for poi in pois:
            poi.imageUrls = session.query(ImageUrls).filter(ImageUrls.poiName == poi.name).all()
        return pois

    @authToken.login_required
    def delete(self, id):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id).filter(InterestPoint.userName == g.user.username).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id))
        session.delete(poi)
        session.commit()
        return {}, 204

@authBasic.verify_password
def verify_password(username, password):
    user = session.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    print(token)
    if user is None:
        return False
    g.user = user
    return True