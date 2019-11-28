from flask import g
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Ramble.Model.model_ramble import RambleDetail, Ramble
import datetime
from src.Ramble.View.ramble_fields import ramble_all
from src.Authentification.authentification import authToken
from src.Configuration.session import session


class RambleRessource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('point', type=dict)
    parser.add_argument('difficulty', type=int)
    parser.add_argument('travel time', type=float)
    parser.add_argument('visible', type=bool)
    parser.add_argument('tag', type=str)

    @authToken.login_required
    @marshal_with(ramble_all)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        difficulty = parsed_args['difficulty']
        travel_time = parsed_args['travel time']
        point = parsed_args['point']
        visible = parsed_args['visible']
        tag = parsed_args['tag']

        username_ramble = session.query(Ramble).filter(Ramble.user_id == g.current_user.id).first()
        name_ramble = session.query(Ramble).filter(Ramble.name == name).first()
        date_n = datetime.datetime.now()
        step = len(point)


        if username_ramble:
            if name_ramble:
                abort(404, message="Vous avez déjà une randonnée du même nom")
        if difficulty < 0 or difficulty > 5 and type(difficulty) == int:
            abort(404, message="la difficulté ne peux aller que de 1 à 5")
        n = Ramble(name=name, username=g.current_user.username, user_id=g.current_user.id, difficulty=difficulty,
                   travel_time=travel_time, step_number=step, date_ramble=date_n, tag=tag)
        if visible is None or False:
            n.visible = True
        for k, id_point in point.items():
            point = RambleDetail(ramble_id=n.id, point_id=id_point, ordre=k)
            n.ramble_detail.append(point)
            session.add(n)
        session.commit()
        return n, 201

    @authToken.login_required
    @marshal_with(ramble_all)
    def get(self):
        rambles = session.query(Ramble).filter(Ramble.user_id == g.current_user.id).all()
        return rambles, 201
