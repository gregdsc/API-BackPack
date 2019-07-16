from Source.Moderation_images.moderate_images import Dectection
from Source.Point.Model import *
from Source.Point.Model.model_point import Point_picture
from Source.User.Model.model_user import *

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from cloudinary import uploader
import re

from Source.Point.View.point_user_field import *
import datetime
from Source.Authentification.Bearer import *
from Source.Point.Model.model_point import *
from Source.User.View.user import *
from Source.Configuration.sight_engine import *

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
        pois = session.query(Interest_point).all()
        return pois

    @authToken.login_required
    @marshal_with(interest_field)
    def post(self):
        parsed_args = self.parser.parse_args()
        name = parsed_args['name']
        description = parsed_args['description']
        lat = parsed_args['lat']
        long = parsed_args['long']
        type = parsed_args['type']
        rank = parsed_args['rank']
        visible = parsed_args['visible']
        date = datetime.datetime.now()


        if name is None or description is None or lat is None or long is None:
            abort(400, message="Missing arguments")
        if session.query(Interest_point).filter(Interest_point.name == name).first() is not None:
            abort(400, message="Poi {} already exists".format(name))
        poi = Interest_point(name=name, description=description, username=g.current_user.username, lat=lat,
                             long=long, type=type, date=date,
                             user_id=g.current_user.id)
        if rank is not None:
            if rank < 1 or rank > 5:
                abort(400, message="rank should be between 1 to 5")
            else:
                poi.rank = rank
        if visible is not None or False:
            poi.visible = True

        if 'images' in request.files:

            image = request.files['images']
            print(image)
            if image.filename != '':
                cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(g.current_user.id,
                                                                                      image.filename))
                output = client_Sight.check('nudity', 'wad', 'scam', 'offensive').set_url(cloudinary_struct['url'])

                j = json.loads(json.dumps(output))
                detection = Dectection(**j)
                if not detection.check_moderate(detection.nudity['raw'],
                                                detection.weapon,
                                                detection.alcohol,
                                                detection.drugs,
                                                detection.scam['prob'],
                                                detection.offensive['prob']):
                    return 'erreur detection'
                picture = Point_picture(url=cloudinary_struct['url'], point_id=poi.id)
                poi.point_picture.append(picture)

        session.add(poi)
        session.commit()
        return poi, 201
