from src.Configuration.session import session
from src.User.Model.model_user import User, UserPicture
from flask_restful import reqparse, abort
from flask_restful import Resource
from flask_restful import marshal_with
from flask_restful import request
from cloudinary import uploader
import re
from src.Email.send_email import send_mail
from src.User.View.user_field import user_fields
from flask import render_template
from src.Moderation_images.moderate_image import moderate_image
from src.Prevision_images.propriete_image import detect_properties_uri
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")



class Utilisateur(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('mail', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('pic_url', type=str)

    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        if not users:
            abort(404, message="Please enter an user before")
        return users

    @marshal_with(user_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        username = parsed_args['username']
        mail = parsed_args['mail']
        password = parsed_args['password']
        description = parsed_args['description']

        if username is None or password is None or mail is None:
            abort(400, message="Missing arguments")

        if not EMAIL_REGEX.match(mail):
            abort(400, message="invalid email address")
        if len(username) < 3:
            abort(400, message="your username must contain at least 3 letters")
        if username == password:
            abort(400, message="Your password, must be different from your username")

        if session.query(User).filter(User.mail == mail).first() is not None:
            abort(400, message="User {} already exists".format(mail))

        mail = mail.lower()

        user = User(username=username, mail=mail)

        if description is not None:
            user.description = description

        if 'image' in request.files:
            image = request.files['image']
            if len(image.filename) >= 120:
                abort(400, message='veuillez renommer votre image, celle-ci ne doit pas dépasser 120 caractère')
            if image.filename != '':
                cloudinary_struct = uploader.upload(image, public_id='{0}_{1}'.format(user.id, image.filename))
                if not moderate_image(cloudinary_struct['url']):
                    abort(401, message="Erreur au niveau de la moderation d'image")
                detect_properties_uri(cloudinary_struct['url'])

                url = UserPicture(url=cloudinary_struct['url'], user_id=user.id)
                user.user_picture.append(url)
        user.hash_password(password)
        session.add(user)
        session.commit()
        try:
            send_mail('noreply.backpack@gmail.com', 'Inscription Backpack',
                      [user.mail], render_template('template_test.html'))
        except:
            abort(403, message='mail non envoyé')
        return user, 201
