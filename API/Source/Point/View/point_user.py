from flask import g
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from cloudinary import uploader
from Source.Authentification.Auth import *
from Source.Point.View.point_user_field import *
from Source.Point.Model.model_point import *


class User_Poi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)

    @marshal_with(interest_field)
    @authToken.login_required
    def get(self):
        pois = session.query(Interest_point).filter(Interest_point.user_id == g.current_user.id).all()
        #for poi in pois:
         # //  poi.imageUrls = session.query(Point_picture).filter(Point_picture.poiName == poi.name).all()
        return pois

    @authToken.login_required
    def delete(id):
        poi = session.query(Interest_point).filter(Interest_point.id == id).filter(Interest_point.user_id ==
                                                                                   g.current_user.id).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id))
        session.delete(poi)
        session.commit()
        return {}, 204