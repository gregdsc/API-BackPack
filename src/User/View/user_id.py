from flask import url_for, g
from src.User.Model.model_user import User, UserPicture
from src.Moderation_images.moderate_image import moderate_image
from src.User.View.user_field import user_fields
from src.Authentification.authentification import authToken
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
import flask_restful
from cloudinary import uploader
from src.Configuration.session import session

class UtilisateurId(Resource):
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
    def delete(self, id_utilisateur):
        user = session.query(User).filter(User.id == id_utilisateur).first()
        if id != g.user.id:
            abort(403, message="user {0} is not allowed to remove user {1}".format(id_utilisateur, g.user.id))
        if not user:
            abort(404, message="user {} doesn't exist".format(id_utilisateur))
        session.delete(user)
        session.commit()
        return {}, 204

    @authToken.login_required
    @marshal_with(user_fields)
    def put(self, id_utilisateur):
        parsed_args = self.parser.parse_args()
        user = session.query(User).filter(User.id == id_utilisateur).first()

        if user.id != g.current_user.id:
            abort(403, message="user {0} is not allowed to modify user {1}".format(id_utilisateur, g.user.id))
        if parsed_args['new_username'] is not None:
            user.username = parsed_args['new_username']
        if parsed_args['new_description'] is not None:
            user.description = parsed_args['new_description']

        if 'image' in flask_restful.request.files:
            image = flask_restful.request.files['image']
            if session.query(UserPicture).filter(UserPicture.user_id == user.id).first() is None:
                images = flask_restful.request.files.getlist('image')
                for image in images:
                    try:
                        cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(user.id, image.filename))
                        url = UserPicture(user_id=user.id, url=cloudinary_struct['url'])
                        if not moderate_image(cloudinary_struct['url']):
                            abort(401, message="Erreur au niveau de la moderation d'image")
                    except:
                        abort(401, message='failed upload file or bad file')
                    user.user_picture.append(url)
                    if session.query(UserPicture).filter(UserPicture.url == url.url).first() is None:
                        session.add(url)
            else:
                url = session.query(UserPicture).filter(UserPicture.user_id == user.id).first()
                if image.filename != '':
                    try:
                        cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(user.id, image.filename))
                        if not moderate_image(cloudinary_struct['url']):
                            abort(401, message="Erreur au niveau de la moderation d'image")
                    except:
                        abort(401, message='failed upload file or bad file')
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
