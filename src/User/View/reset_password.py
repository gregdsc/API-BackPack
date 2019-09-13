from flask import current_app, render_template
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from src.User.Model.model_user import *
from src.Email.send_email import send_mail
from src.Configuration.session import session
from flask_restful import reqparse, abort
from flask_restful import Resource
from flask import render_template

class Reset_Password(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mail', type=str)
    parser.add_argument('new_password', type=str)
    parser.add_argument('new_password_confirmation', type=str)
    parser.add_argument('token', type=str)

    def post(self):
        parsed_args = self.parser.parse_args()
        if session.query(User).filter(User.mail == parsed_args['mail']).first() is not None:
            user = session.query(User).filter(User.mail == parsed_args['mail']).first()
            user.token_reset_password = user.generate_reset_token()
            session.add(user)
            session.commit()
            reset_link = "http://localhost:5000/reset_password?token=" + user.token_reset_password
            try:
                send_mail('noreply.backpack@gmail.com', 'Reinitialiser votre mot de passe',
                          [parsed_args['mail']], render_template("template_reset_mail.html",
                                                                              link=reset_link))
            except:
                abort(400, message='mail non envoyé')
            return 201
        else:
            abort(400, message='le mail nexiste pas')

    def put(self):
        parsed_args = self.parser.parse_args()
        s = Serializer(current_app.config['SECRET_KEY'])
        user = session.query(User).filter(User.token_reset_password == parsed_args['token']).first()
        if user is not None:
            if user.username == parsed_args['new_password']:
                abort(400, message="Your password, must be different from your username")
            if parsed_args['new_password'] == parsed_args['new_password_confirmation']:
                user.hash_password(parsed_args['new_password'])
                session.add(user)
                session.commit()
            return 201