from src.Configuration.session import session
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from src.Ramble.View.ramble_fields import fields
from src.Ramble.Model.model_ramble import Ramble


class RambleVisibleUser(Resource):

    @marshal_with(fields)
    def get(self, id):
        ramble_visible = session.query(Ramble).filter(Ramble.user_id == id). \
            filter(Ramble.visible is True).all()
        if not ramble_visible:
            abort(401, message='No ramble for this user')
        return ramble_visible
