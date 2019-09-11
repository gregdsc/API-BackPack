from flask import g
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
import flask_restful
from cloudinary import uploader
from src.Point.View.point_user_field import interest_field
from src.Authentification.authentification import authToken
from src.Point.View.interest_point import InterestPoint
from src.Moderation_images.moderate_image import moderate_image
from src.Configuration.session import session

class PointId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)
    parser.add_argument('rank', type=int)
    parser.add_argument('visible', type=bool)

    @marshal_with(interest_field)
    def get(self, id_point):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id_point).first()
        if not poi:
            abort(404, message="poi {} doesn't exist".format(id_point))
        return poi

    @staticmethod
    @authToken.login_required
    def delete(id_point):
        poi = session.query(InterestPoint).filter(InterestPoint.id == id_point).first()
        if poi.user_id == g.current_user.id:
            if not poi:
                abort(404, message="poi {} doesn't exist".format(id_point))
            session.delete(poi)
            session.commit()
        else:
            abort(400, message="This point isn't yours")
        return {}, 204

    @marshal_with(interest_field)
    @authToken.login_required
    def put(self, id_point):
        parsed_args = self.parser.parse_args()
        poi = session.query(InterestPoint).filter(InterestPoint.id == id_point).first()

        if poi.user_id == g.current_user.id:
            if parsed_args['name'] is not None:
                poi.name = parsed_args['name']
            if parsed_args['description'] is not None:
                poi.description = parsed_args['description']
            if parsed_args['lat'] is not None:
                poi.lat = parsed_args['lat']
            if parsed_args['long'] is not None:
                poi.long = parsed_args['long']
            if parsed_args['visible'] is not None:
                poi.visible = parsed_args['visible']
            if parsed_args['rank'] is not None:
                rank = parsed_args['rank']
                if rank is not None:
                    if rank < 1 or rank > 5:
                        abort(400, message="rank should be between 1 to 5")
                    else:
                        poi.rank = rank

            if 'image' in flask_restful.request.files:
                image = flask_restful.request.files['image']
                if session.query(InterestPoint).filter(InterestPoint.point_id == id_point).first() is None:
                    images = flask_restful.request.files.getlist('image')
                    for image in images:
                        try:
                            cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                              image.filename))
                            if not moderate_image(cloudinary_struct['url']):
                                abort(401, message="Erreur au niveau de la moderation d'image")
                        except:
                            abort(401, message='failed upload file or bad file')
                        url = InterestPoint(point_id=poi.id, url=cloudinary_struct['url'])
                        poi.point_picture.append(url)
                        if session.query(InterestPoint).filter(InterestPoint.url == url.url).first() is None:
                            session.add(url)
                else:
                    url = session.query(InterestPoint).filter(InterestPoint.point_id == id_point).first()
                    if image.filename != '':
                        try:
                            cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                              image.filename))
                            if not moderate_image(cloudinary_struct['url']):
                                abort(401, message="Erreur au niveau de la moderation d'image")
                        except:
                            abort(401, message='failed upload file or bad file')
                        url.url = cloudinary_struct['url']
                        poi.point_picture.append(url)

            session.add(poi)
            session.commit()
        else:
            abort(400, message="This point isn't yours")

        return poi, 201
