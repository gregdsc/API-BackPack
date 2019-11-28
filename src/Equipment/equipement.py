from flask import jsonify
from flask_restful import Resource, abort
from src.Configuration.session import session
from src.Ramble.Model.model_ramble import Ramble
from src.Equipment.list_equipment import standard, experimente, experimente_nuit

class EquipmentRessource(Resource):
    def get(self, id):
        equipement = session.query(Ramble).filter(Ramble.id == id).first()
        if equipement is None:
            abort(404, message="No ramble")
        if equipement.tag == "standard":
            return jsonify(standard)
        if equipement.tag == "expert":
            return jsonify(experimente)
        if equipement.tag == "expert_nuit":
            return jsonify(experimente_nuit)
        else:
            return "Your ramble hasn't tag or specification"