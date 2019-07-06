from Source.Ramble.Model.model_ramble import *
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import marshal_with
from Source.Ramble.Model.model_ramble import *
import datetime
from Source.Ramble.View.ramble_fields import *
from Source.Authentification.Bearer import *
from Source.Point.View.interest_point_id import *

class Id_ramble(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)

    @authToken.login_required
    @marshal_with(ramble)
    def get(self, id):
        rando = session.query(Ramble).filter(Ramble.id == id).filter(Ramble.user_id == g.current_user.id).first()
        if rando is None:
            return 200, "You don't have a hike"
        rando_details = session.query(Ramble_detail.point_id).filter(Ramble_detail.ramble_id == id)\
            .order_by(Ramble_detail.ordre).all()
        len_rand = len(rando_details)
        i = 0
        points = []
        while i < len_rand:
            p = Point_id.get(self, rando_details[i])
            points.append(p)
            i += 1
        rando.point_id = points
        return rando

    def delete(self, id):
        rando = session.query(Ramble_detail).filter(Ramble_detail.ramble_id == id).delete()
        ramble = session.query(Ramble).filter(Ramble.id == id).delete()
        return 201

class Point_in_Ramble(Resource):

    @authToken.login_required
    def delete(self, id, id_point):
        rando = session.query(Ramble).filter(Ramble.id == id).filter(Ramble.user_id == g.current_user.id).first()
        rando_details = session.query(Ramble_detail).filter(Ramble_detail.ramble_id == rando.id).filter(Ramble_detail.point_id == id_point).delete()
        session.commit()
        return {}, 204