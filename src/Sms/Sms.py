from flask_restful import Resource
from twilio.rest import Client
# Your Account Sid and auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
class Envoi_sms(Resource):
    def get(self):
        account_sid = 'AC7ab3056ccd81919aca1b8439f74e07ad'
        auth_token = 'ba728173e4c5e8164528684dc5435d77'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Cela fait un bail que l'on ne vous a pas vu :) Venez préparer votre prochaine randonnée",
            from_='+33644600638',
            to='+33667017109'
        )
        return 200