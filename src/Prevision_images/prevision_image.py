from src.User.Model.model_user import User, UserPicture
from flask_restful import reqparse, abort, Resource
from flask_restful import request
from cloudinary import uploader
from src.Moderation_images.moderate_image import moderate_image
from src.Prevision_images.propriete_image import detect_web_uri


# test encore beaucoup de choses à modifier

class PrevisionImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('mail', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('pic_url', type=str)

    def post(self):
        parsed_args = self.parser.parse_args()
        username = parsed_args['username']
        mail = parsed_args['mail']
        password = parsed_args['password']
        description = parsed_args['description']
        dict = {}

        if 'image' in request.files:
            image = request.files['image']
            if len(image.filename) >= 120:
                abort(400, message='veuillez renommer votre image, celle-ci ne doit pas dépasser 120 caractère')
            if image.filename != '':
                try:
                    cloudinary_struct = uploader.upload(image, public_id='{0}'.format(image.filename))
                    if not moderate_image(cloudinary_struct['url']):
                        abort(401, message="Erreur au niveau de la moderation d'image")
                    dict = detect_web_uri(cloudinary_struct['url'])
                except:
                    abort(401, message='failed upload file or bad file')
        return dict
