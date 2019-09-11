from flask import g
from src.Moderation_images.moderate_image import moderate_image
from src.Point.Model.model_point import InterestPoint, PointPicture
from src.Configuration.session import session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
import flask_restful
from cloudinary import uploader
from src.Point.View.point_user_field import interest_field
import datetime
from src.Authentification.authentification import authToken
from src.Configuration.sight_engine import client_Sight


class Point(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('lat', type=float)
    parser.add_argument('long', type=float)
    parser.add_argument('type', type=str)
    parser.add_argument('rank', type=int)
    parser.add_argument('visible', type=bool)

    @marshal_with(interest_field)
    def get(self):
        pois = session.query(InterestPoint).all()
        return pois

    @authToken.login_required
    @marshal_with(interest_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        description = parsed_args['description']
        lat = parsed_args['lat']
        long = parsed_args['long']
        type_point = parsed_args['type']
        rank = parsed_args['rank']
        visible = parsed_args['visible']
        date = datetime.datetime.now()

        if name is None or description is None or lat is None or long is None:
            abort(400, message="Missing arguments")
        if session.query(InterestPoint).filter(InterestPoint.name == name).first() is not None:
            abort(400, message="Poi {} already exists".format(name))
        poi = InterestPoint(name=name, description=description, username=g.current_user.username, lat=lat,
                            long=long, type=type_point, date=date,
                            user_id=g.current_user.id)
        if rank is not None:
            if rank < 1 or rank > 5:
                abort(400, message="rank should be between 1 to 5")
            else:
                poi.rank = rank
        if visible is None or False:
            poi.visible = True

        if 'images' in flask_restful.request.files:

            image = flask_restful.request.files['images']
            print(image)
            if image.filename != '':
                try:
                    cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                      image.filename))
                    if not moderate_image(cloudinary_struct['url']):
                        abort(401, message="Erreur au niveau de la moderation d'image")
                except:
                    abort(401, message='failed upload file or bad file')
                picture = PointPicture(url=cloudinary_struct['url'], point_id=poi.id)
                poi.point_picture.append(picture)

        session.add(poi)
        session.commit()
        return poi, 201
