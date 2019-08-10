from flask_restful import fields

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password_hash': fields.String,
    'description': fields.String,
    'user_picture': fields.List(fields.String(attribute='url')),
    'uri': fields.Url('user', absolute=True),
}