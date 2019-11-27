from flask import g
from src.Ramble.Model.model_ramble import Ramble, RambleDetail
from flask_restful import reqparse, abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Ramble.View.ramble_fields import ramble
from src.Authentification.authentification import authToken
from src.Point.View.interest_point_id import PointId
from src.Configuration.session import session


class RambleId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)

    @authToken.login_required
    @marshal_with(ramble)
    def get(self, id_ramble):
        rando = session.query(Ramble).filter(Ramble.id == id_ramble).filter(Ramble.user_id == g.current_user.id).first()
        if rando is None:
            return 200, "You don't have a hike"
        rando_details = session.query(RambleDetail.point_id).filter(RambleDetail.ramble_id == id_ramble) \
            .order_by(RambleDetail.ordre).all()
        len_rand = len(rando_details)
        i = 0
        points = []
        while i < len_rand:
            p = PointId.get(self, rando_details[i])
            points.append(p)
            i += 1
        rando.point_id = points
        return rando

    @authToken.login_required
    def delete(self, id):
        ramble = session.query(Ramble).filter(Ramble.id == id).first()
        if ramble.user_id == g.current_user.id:
            if not ramble:
                abort(404, message="poi {} doesn't exist".format(id))
            session.delete(ramble)
            session.commit()
        else:
            abort(400, message="This point isn't yours")
        return {}, 204
