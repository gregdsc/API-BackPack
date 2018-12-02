from flask import g
from db import session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from manage import Activity, User, Ramble, ImageUrls, InterestPoint

ramble_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'point': fields.Integer,
    'number_poi': fields.Integer,
    'imageUrls': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('user', absolute=True),
}


class ramble_ressource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)

    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        point = {"campement": 123,
                 "vue du mont": 11,
                 "feu de bois":12333
        }
        if name is None:
           for x in point:
               print [x]
        if point is None:
            abort(403, message="impossible de crée une rando si il n'existe pas de point de départ")
        point_q = point(point=point)
        session.add(point_q)
        return point_q, 201
