from flask import url_for

from Source.User.Model.model_user import *
from Source.User.View.user import *
from Source.User.View.user_field import *
from Source.Authentification.Auth import *

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import request
from cloudinary import uploader

class Utilisateur_id(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_username', type=str)
    parser.add_argument('new_password', type=dict)
    parser.add_argument('new_description', type=str)
    parser.add_argument('new_pic_url', type=str)

    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="user {} doesn't exist".format(id))
        return user

    @authToken.login_required
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if id != g.user.id:
            abort(403, message="user {0} is not allowed to remove user {1}".format(id, g.user.id))
        if not user:
            abort(404, message="user {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @authToken.login_required
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = self.parser.parse_args()
        user = session.query(User).filter(User.id == id).first()

        if user.id != g.current_user.id:
            abort(403, message="user {0} is not allowed to modify user {1}".format(id, g.user.id))
        if parsed_args['new_username'] is not None:
            user.username = parsed_args['new_username']
        if parsed_args['new_description'] is not None:
            user.description = parsed_args['new_description']

        if 'image' in request.files:
            image = request.files['image']
            if session.query(User_picture).filter(User_picture.user_id == user.id).first() is None:
                images = request.files.getlist('image')
                for image in images:
                    cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(user.id, image.filename))
                    url = User_picture(user_id=user.id, url=cloudinary_struct['url'])
                    output = client.check('nudity', 'wad', 'scam', 'offensive').set_url(cloudinary_struct['url'])

                    j = json.loads(json.dumps(output))
                    detection = Dectection(**j)
                    if not detection.check_moderate(detection.nudity['raw'],
                                                    detection.weapon,
                                                    detection.alcohol,
                                                    detection.drugs,
                                                    detection.scam['prob'],
                                                    detection.offensive['prob']):
                        return 'erreur detection'
                    user.user_picture.append(url)
                    if session.query(User_picture).filter(User_picture.url == url.url).first() is None:
                        session.add(url)
            else:
                url = session.query(User_picture).filter(User_picture.user_id == user.id).first()
                if image.filename != '':
                    cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(user.id, image.filename))
                    output = client.check('nudity', 'wad', 'scam', 'offensive').set_url(cloudinary_struct['url'])

                    j = json.loads(json.dumps(output))
                    detection = Dectection(**j)
                    if not detection.check_moderate(detection.nudity['raw'],
                                                    detection.weapon,
                                                    detection.alcohol,
                                                    detection.drugs,
                                                    detection.scam['prob'],
                                                    detection.offensive['prob']):
                        return 'erreur detection'
                    url.url = cloudinary_struct['url']
                    user.user_picture.append(url)

        if parsed_args['new_password'] is not None:
            password_reset = parsed_args['new_password']
            if not user.verify_password(password_reset['old_password']) or password_reset['new_password'] != \
                    password_reset['new_password_confirm']:
                abort(400, message="wrong old_password or new_password and new_password_confirm mismatch")
            user.hash_password(password_reset['new_password'])
        session.add(user)
        session.commit()
        return user, 201