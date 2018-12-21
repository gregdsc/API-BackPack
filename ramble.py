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
from manage import *
from resources import InterestPointRessource, InterestPointListRessource
import datetime

point = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'lat': fields.Float,
        'long': fields.Float,
        'userName': fields.String,
        'type': fields.String,
        'date': fields.DateTime,
        'rank': fields.Integer,
        'imageUrls': fields.List(fields.String(attribute='url')),
    }

ramble = {
    'id': fields.Integer,
    'name': fields.String,
    'point':fields.Nested(point),
    'uri': fields.Url('rambles', absolute=True),
}


ramble_all = {
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.DateTime(attribute='date_ramble'),
    'difficulty': fields.Integer,
    'travel time': fields.Float(attribute='travel_time'),
    'step number': fields.Float(attribute='step_number'),
    'imageUrls': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('rambles', absolute=True),
}

authBasic = HTTPBasicAuth()
authToken = HTTPTokenAuth()

class Ramble_ressource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)


    @marshal_with(ramble)
    def get(self, id):
        rando = session.query(Ramble).filter(Ramble.id == id).first()
        rando_details = session.query(Ramble_details.point).filter(Ramble_details.id_ramble == id).order_by(Ramble_details.ordre).all()
        len_rand = len(rando_details)
        i = 0
        points = []
        while i < len_rand:
            p = InterestPointRessource.get(self, rando_details[i])
            points.append(p)
            i += 1
        rando.point = points
        return rando

    def delete(id, id_point):
        rando = session.query(Ramble).filter(Ramble.id == id).first()
        rando_details = session.query(Ramble_details.point).filter(Ramble_details.point == id_point).delete()
        session.commit()
        return {}, 204



class Ramble_List_ressource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)
    parser.add_argument('difficulty', type=int)
    parser.add_argument('travel time', type=float)

    @authToken.login_required
    @marshal_with(ramble_all)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        difficulty = parsed_args['difficulty']
        travel_time = parsed_args['travel time']
        point = parsed_args['point']

        username_ramble = session.query(Ramble).filter(Ramble.userName == g.user.username).first()
        name_ramble = session.query(Ramble).filter(Ramble.name == name).first()
        date_n = datetime.datetime.now()
        step = len(point)

        if username_ramble:
            if name_ramble:
                abort(404, message="Vous avez déjà une randonnée du même nom")
        if difficulty < 0 or difficulty > 5 and type(difficulty) == int:
            abort(404, message="la difficulté ne peux aller que de 1 à 5 et doit être un int")
        n = Ramble(name=name, userName=g.user.username, difficulty=difficulty, travel_time=travel_time, step_number=step, date_ramble=date_n)
        session.add(n)
        session.commit() # à voir si on fait une relation de model plus besoin de commit. pour récupérer l'id
        n2 = session.query(Ramble).filter(Ramble.name == name).first()
        for k, id_point in point.items():
            point = Ramble_details(id_ramble=n2.id, point=id_point, ordre=k)
            session.add(point)
        session.commit()
        return n, 201

    @authToken.login_required
    @marshal_with(ramble_all)
    def get(self):
        rambles = session.query(Ramble).filter(Ramble.userName == g.user.username).order_by(Ramble.date_ramble.desc()).all()
        return rambles, 201

    #@authToken.login_required
    #def delete(self):
     #   rambles = session.query(Ramble).filter(Ramble.userName == g.user.username).delete()
      #  session.commit()
       # return {}, 201


@authToken.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is None:
        return False
    g.user = user
    return True
