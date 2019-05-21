from Source.Point.Model import *
from Source.Point.Model.model_point import Point_picture
from Source.User.Model.model_user import *

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import request
from cloudinary import uploader
from Source.Point.View.point_user_field import *

from Source.Authentification.Auth import *
from Source.Point.Model.model_point import *

class Point_id(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)
    parser.add_argument('rank', type=int)


    @marshal_with(interest_field)
    def get(self, id):
        poi = session.query(Interest_point).filter(Interest_point.id == id).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id))
        return poi

    @staticmethod
    @authToken.login_required
    def delete(id):
        poi = session.query(Interest_point).filter(Interest_point.id == id).first()
        if poi.user_id == g.current_user.id:
            if not poi:
                abort(404, message="poi {} doesn't exist".format(id))
            session.delete(poi)
            session.commit()
        else:
            abort(400, message="This point isn't yours")
        return {}, 204

    @marshal_with(interest_field)
    @authToken.login_required
    def put(self, id):
        parsed_args = self.parser.parse_args()
        poi = session.query(Interest_point).filter(Interest_point.id == id).first()

        if poi.user_id == g.current_user.id:
            if parsed_args['name'] is not None:
                poi.name = parsed_args['name']
            if parsed_args['description'] is not None:
                poi.description = parsed_args['description']
            if parsed_args['lat'] is not None:
                poi.lat = parsed_args['lat']
            if parsed_args['long'] is not None:
                poi.long = parsed_args['long']
            if parsed_args['rank'] is not None:
                rank = parsed_args['rank']
                if rank is not None:
                    if rank < 1 or rank > 5:
                        abort(400, message="rank should be between 1 to 5")
                    else:
                        poi.rank = rank

            if 'image' in request.files:
                image = request.files['image']
                if session.query(Point_picture).filter(Point_picture.point_id == id).first() is None:
                    images = request.files.getlist('image')
                    for image in images:
                        cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                              image.filename))
                        url = Point_picture(point_id=poi.id, url=cloudinary_struct['url'])
                        poi.point_picture.append(url)
                        if session.query(Point_picture).filter(Point_picture.url == url.url).first() is None:
                            session.add(url)
                else:
                    url = session.query(Point_picture).filter(Point_picture.point_id == id).first()
                    if image.filename != '':
                        cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                              image.filename))
                        url.url = cloudinary_struct['url']
                        poi.point_picture.append(url)

            session.add(poi)
            session.commit()
        else:
            abort(400, message="This point isn't yours")

        return poi, 201