from flask import g
from db import session
import json
import re
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from manage import Activity, User, Ramble, ImageUrls, InterestPoint
from resources import InterestPointRessource

ramble_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'point': fields.String,
    'uri': fields.Url('rambles', absolute=True),
}

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()

class Ramble_ressource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)

    @authToken.login_required
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        point = parsed_args['point']

        x = '1'
        rando_fields = {'name': fields.String}
        rando_fields['Point_interet']={}
        rando_fields['Point_interet']['name_poi' + x] = fields.String(attribute="")


        str_point = json.dumps(point)
        print(str_point)
        if not point:
            abort(403, message="impossible de créer une rando si il n'existe pas de point de départ")
        if name is None:
            name = ", ".join(point.keys())
        rando = Ramble(name=name, point=str_point, userName=g.user.username)
        session.add(rando)
        session.commit()
        return rando



    def get(self, id):
        resource_fields = {'name': fields.String}
        resource_fields['point_interet'] = {}
        resource_fields['point_interet']['id'] = fields.Integer
        resource_fields['point_interet']['name'] = fields.String(attribute='name')
        resource_fields['point_interet']['description'] = fields.String
        resource_fields['point_interet']['lat'] = fields.Float
        resource_fields['point_interet']['long'] = fields.Float
        resource_fields['point_interet']['type'] = fields.String

        data = InterestPointRessource().get(74)
        data1 = InterestPointRessource().get(75)
        data2 = InterestPointRessource().get(76)
        a = marshal(data, resource_fields)
        b = marshal(data, resource_fields)
        print(a)
        return a, b







        rando = session.query(Ramble).filter(Ramble.id == id).first()


        point = session.query(Ramble.point).filter(Ramble.id == id).first()

        return rando

        point = session.query(InterestPoint).filter(InterestPoint.id == id_point).first()
        point.imageUrls = session.query(ImageUrls).filter(ImageUrls.poiName == poi.name).all()
        return "ok"

@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True