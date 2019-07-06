import base64

from googleapiclient import discovery

from Source.User.Model.model_user import *
from flask import json
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from flask_restful import request
from cloudinary import uploader
import re
from Source.Email.send_email import *
from Source.User.View.user_field import *
from flask import render_template
from Source.Configuration.sight_engine import *
from Source.Moderation_images.moderate_images import *

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

import json

def vision_image_manager(image_file):
    # Instantiates a client
    service = discovery.build('vision', 'v1', credentials=credentials)
    # text.png is the image file.


    file_name = str(image_file)
    print(file_name)
    with open(file_name, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                }]
            }]
        })
    response = service_request.execute()
    print(response['responses'])
    res_dict = dict(response)
    return res_dict


# Parse JSON into an object with attributes corresponding to dict keys.

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision, language
from google.cloud.vision import types
from google.cloud.language import enums, types
from google.oauth2 import service_account




#credentials = service_account.Credentials. from_service_account_file(r'C:\Users\Alexandre\Desktop\project.json')
# Instantiates a client
#clients = vision.ImageAnnotatorClient(credentials=credentials)




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
                #vision_image_manager(r'C:\Users\Alexandre\Desktop\rose.jpeg')

                url = User_picture(url=cloudinary_struct['url'], user_id=user.id)
                user.user_picture.append(url)
        user.hash_password(password)
        session.add(user)
        session.commit()

        send_mail('noreply.backpack@gmail.com', 'Inscription Backpack',
                  [user.mail], render_template('template_test.html'))

        return user, 201