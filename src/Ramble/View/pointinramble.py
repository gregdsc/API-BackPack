from flask_restful import Resource
from src.Authentification.authentification import authToken
from src.Configuration.session import session
from src.Ramble.Model.model_ramble import Ramble, RambleDetail


class PointInRamble(Resource):

    @authToken.login_required
    def delete(self, id_ramble, id_point):
        rando = session.query(Ramble).filter(Ramble.id == id_ramble).filter(Ramble.user_id == g.current_user.id).first()
        rando_details = session.query(RambleDetail).filter(RambleDetail.ramble_id == rando.id) \
            .filter(RambleDetail.point_id == id_point).delete()
        session.commit()
        return {}, 204
