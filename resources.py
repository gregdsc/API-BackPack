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

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password_change', type=dict)

    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="user {} doesn't exist".format(id))
        return user

    @authToken.login_required
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if id != g.user.id:
            abort(403, message="user {0} is not allowed to remove user {1}".format(id, g.user.id))
        if not user:
            abort(404, message="user {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @authToken.login_required
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = self.parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        if user.id != g.user.id:
            abort(403, message="user {0} is not allowed to modify user {1}".format(id, g.user.id))
        if parsed_args['username'] is not None:
            user.username = parsed_args['username']
            print("lel")
        if parsed_args['password_change'] is not None:
            password_reset = parsed_args['password_change']
            if not user.verify_password(password_reset['old_password']) or password_reset['new_password'] != \
                    password_reset['new_password_confirm']:
                abort(400, message="wrong old_password or new_password and new_password_confirm mismatch")
            user.hash_password(password_reset['new_password'])
        session.add(user)
        session.commit()
        return user, 201


class UserListRessource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)

    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        if not users:
            abort(404, message="Please enter an user before")
        return users

    @marshal_with(user_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        username = parsed_args['username']
        password = parsed_args['password']
        if username is None or password is None:
            abort(400, message="Missing arguments")
        if session.query(User).filter(User.username == username).first() is not None:
            abort(400, message="User {} already exists".format(username))
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        return user, 201


class InterestPointRessource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)


    @marshal_with(interest_field)
    def get(self, type):
        poi = session.query(InterestPoint).filter(InterestPoint.type == type).all()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(type))
        return poi

    @marshal_with(interest_field)
    def get(self, id):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id))
        return poi

    @staticmethod
    def delete(id):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id))
        session.delete(poi)
        session.commit()
        return {}, 204

    @marshal_with(interest_field)
    def put(self, id):
        parsed_args = self.parser.parse_args()
        poi = session.query(InterestPoint).filter(InterestPoint.id == id).first()
        poi.name = parsed_args['name']
        poi.description = parsed_args['description']
        poi.lat = parsed_args['lat']
        poi.long = parsed_args['long']
        session.add(poi)
        session.commit()
        return poi, 201


class InterestPointListRessource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)

    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).all()
        for poi in pois:
            # print(poi.imageUrls)
            poi.imageUrls = session.query(ImageUrls).filter(ImageUrls.poiName == poi.name).all()
            # print(poi.imageUrls)
        return pois

    @authToken.login_required
    @marshal_with(interest_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        description = parsed_args['description']
        lat = parsed_args['lat']
        long = parsed_args['long']
        type = parsed_args['type']
        if name is None or description is None or lat is None or long is None:
            abort(400, message="Missing arguments")
        if session.query(InterestPoint).filter(InterestPoint.name == name).first() is not None:
            abort(400, message="Poi {} already exists".format(name))
        poi = InterestPoint(name=name, description=description, lat=lat,
                            long=long, type=type, userName=g.user.username)
        session.add(poi)
        poi.imageUrls = []
        images = request.files.getlist('images')
        for image in images:
            oader.uploadcloudinary_struct = upl(image, public_id='{0}_{1}_{2}'.format(g.user.username, name,
                                                                                      image.filename))
            print(cloudinary_struct)
            url = ImageUrls(url=cloudinary_struct['url'], poiName=name)
            poi.imageUrls.append(url)
            if session.query(ImageUrls).filter(ImageUrls.url == url.url).first() is None:
                session.add(url)
        session.commit()
        return poi, 201


class GetToken(Resource):
    @authBasic.login_required
    def get(self):
        token = g.user.generate_auth_token(expiration=10000)
        return {'token': token.decode('ascii')}


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
    if user is None:
        return False
    g.user = user
    return True
